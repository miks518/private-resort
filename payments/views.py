from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
from reservations.models import Reservation
from .models import Payment
from .services import create_checkout_session, retrieve_checkout_session


@login_required
def initiate_payment(request, reservation_pk):
    """
    Validate payment and create a PayMongo checkout session (Process 3.1, 3.2).
    """
    reservation = get_object_or_404(
        Reservation, pk=reservation_pk, user=request.user
    )

    if reservation.status not in [Reservation.Status.PENDING, Reservation.Status.CONFIRMED]:
        messages.error(request, 'This reservation cannot be paid for at this time.')
        return redirect('reservations:detail', pk=reservation.pk)

    # Create or get existing pending payment
    payment, created = Payment.objects.get_or_create(
        reservation=reservation,
        status=Payment.Status.PENDING,
        defaults={
            'user': request.user,
            'amount': reservation.total_price,
        }
    )

    if not settings.PAYMONGO_SECRET_KEY:
        # Sandbox / dev mode — skip PayMongo and simulate success
        messages.warning(
            request,
            'PayMongo is not configured. Payment simulated for development.'
        )
        payment.status = Payment.Status.PAID
        payment.paid_at = timezone.now()
        payment.generate_receipt_number()
        payment.save()
        reservation.status = Reservation.Status.PAID
        reservation.save()
        return redirect('payments:success', pk=payment.pk)

    # Build success/cancel URLs
    success_url = request.build_absolute_uri(f'/payments/{payment.pk}/verify/')
    cancel_url = request.build_absolute_uri(f'/reservations/{reservation.pk}/')

    checkout_id, checkout_url = create_checkout_session(
        payment, success_url, cancel_url
    )

    if checkout_url:
        payment.paymongo_checkout_id = checkout_id
        payment.checkout_url = checkout_url
        payment.status = Payment.Status.PROCESSING
        payment.save()
        return redirect(checkout_url)
    else:
        messages.error(request, 'Unable to create payment session. Please try again.')
        return redirect('reservations:detail', pk=reservation.pk)


@login_required
def verify_payment(request, pk):
    """
    Verify payment after PayMongo redirect (Process 3.3).
    """
    payment = get_object_or_404(Payment, pk=pk, user=request.user)

    if payment.paymongo_checkout_id:
        session_data = retrieve_checkout_session(payment.paymongo_checkout_id)
        if session_data:
            status = session_data['attributes'].get('payment_intent', {}).get('attributes', {}).get('status', '')
            if status == 'succeeded':
                payment.status = Payment.Status.PAID
                payment.paid_at = timezone.now()
                payment.generate_receipt_number()
                payment.save()
                payment.reservation.status = Reservation.Status.PAID
                payment.reservation.save()
                return redirect('payments:success', pk=payment.pk)

    # If verification fails or is still processing
    messages.info(request, 'Payment is being processed. Please check back shortly.')
    return redirect('reservations:detail', pk=payment.reservation.pk)


@login_required
def payment_success(request, pk):
    """Display payment receipt (Process 3.4)."""
    payment = get_object_or_404(Payment, pk=pk, user=request.user, status=Payment.Status.PAID)

    return render(request, 'payments/success.html', {
        'payment': payment,
    })


@login_required
def payment_history(request):
    """Show all payments for the logged-in user."""
    payments = Payment.objects.filter(user=request.user)
    return render(request, 'payments/history.html', {
        'payments': payments,
    })


@csrf_exempt
def paymongo_webhook(request):
    """
    Handle PayMongo webhook events for automatic payment status updates.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    import json
    try:
        body = json.loads(request.body)
        event_type = body['data']['attributes']['type']

        if event_type == 'checkout_session.payment.paid':
            checkout_data = body['data']['attributes']['data']
            checkout_id = checkout_data['id']

            try:
                payment = Payment.objects.get(paymongo_checkout_id=checkout_id)
                payment.status = Payment.Status.PAID
                payment.paid_at = timezone.now()
                payment.generate_receipt_number()
                payment.save()
                payment.reservation.status = Reservation.Status.PAID
                payment.reservation.save()
            except Payment.DoesNotExist:
                pass

        return JsonResponse({'status': 'ok'})
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Invalid payload'}, status=400)
