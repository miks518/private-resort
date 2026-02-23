from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from facilities.models import Facility
from .models import Reservation
from .forms import ReservationForm


@login_required
def check_availability(request, facility_slug):
    """Check available dates for a facility (Process 2.1)."""
    facility = get_object_or_404(Facility, slug=facility_slug, is_available=True)

    # Get existing confirmed/paid reservations for this facility
    existing_reservations = Reservation.objects.filter(
        facility=facility,
        status__in=[Reservation.Status.CONFIRMED, Reservation.Status.PAID],
    ).values('check_in', 'check_out')

    return render(request, 'reservations/check_availability.html', {
        'facility': facility,
        'existing_reservations': list(existing_reservations),
    })


@login_required
def create_reservation(request, facility_slug):
    """Create a new reservation (Process 2.2)."""
    facility = get_object_or_404(Facility, slug=facility_slug, is_available=True)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.facility = facility

            # Check for date conflicts
            conflicts = Reservation.objects.filter(
                facility=facility,
                status__in=[
                    Reservation.Status.CONFIRMED,
                    Reservation.Status.PAID,
                ],
            ).filter(
                Q(check_in__lt=reservation.check_out) &
                Q(check_out__gt=reservation.check_in)
            )

            if conflicts.exists():
                messages.error(
                    request,
                    'The selected dates are not available. Please choose different dates.'
                )
                return render(request, 'reservations/create_reservation.html', {
                    'form': form, 'facility': facility,
                })

            # Check guest capacity
            if reservation.guests > facility.capacity:
                messages.error(
                    request,
                    f'This facility can accommodate a maximum of {facility.capacity} guests.'
                )
                return render(request, 'reservations/create_reservation.html', {
                    'form': form, 'facility': facility,
                })

            reservation.calculate_total()
            reservation.save()
            messages.success(request, 'Reservation created! Please proceed to payment.')
            return redirect('reservations:detail', pk=reservation.pk)
    else:
        form = ReservationForm()

    return render(request, 'reservations/create_reservation.html', {
        'form': form,
        'facility': facility,
    })


@login_required
def reservation_detail(request, pk):
    """View reservation details (Process 2.3 — Confirm Booking)."""
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)

    return render(request, 'reservations/reservation_detail.html', {
        'reservation': reservation,
    })


@login_required
def cancel_reservation(request, pk):
    """Cancel a reservation (Process 2.4)."""
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)

    if reservation.status in [Reservation.Status.PENDING, Reservation.Status.CONFIRMED]:
        if request.method == 'POST':
            reservation.status = Reservation.Status.CANCELLED
            reservation.save()
            messages.success(request, 'Your reservation has been cancelled.')
            return redirect('reservations:my_reservations')
    else:
        messages.error(request, 'This reservation cannot be cancelled.')

    return render(request, 'reservations/cancel_reservation.html', {
        'reservation': reservation,
    })


@login_required
def my_reservations(request):
    """List all reservations for the logged-in user."""
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'reservations/my_reservations.html', {
        'reservations': reservations,
    })
