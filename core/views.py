from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from facilities.models import Facility


def home(request):
    featured_facilities = Facility.objects.filter(is_available=True)[:6]
    return render(request, 'core/home.html', {
        'featured_facilities': featured_facilities,
    })


def about(request):
    return render(request, 'core/about.html')


def amenities(request):
    return render(request, 'core/amenities.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_body = request.POST.get('message', '').strip()

        if not name or not email or not message_body:
            messages.error(request, 'Please fill in your name, email, and message.')
            return redirect('core:contact')

        if settings.EMAIL_HOST_USER:
            try:
                send_mail(
                    subject=f"[Resort Contact] {subject or 'No Subject'}",
                    message=f"From: {name} <{email}>\n\n{message_body}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
            except Exception:
                messages.warning(
                    request,
                    'We received your message but could not send a confirmation email. '
                    'We will get back to you soon!'
                )
                return redirect('core:contact')

        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('core:contact')

    return render(request, 'core/contact.html')
