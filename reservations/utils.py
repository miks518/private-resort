import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

def notify_admin_booking_created(reservation):
    """Notify the admin when a new reservation is created."""
    if not settings.EMAIL_HOST_USER:
        return

    subject = f"[New Booking] Reservation #{reservation.pk} created by {reservation.user.get_full_name() or reservation.user.username}"
    message = (
        f"A new reservation has been created.\n\n"
        f"Reservation ID: #{reservation.pk}\n"
        f"User: {reservation.user.get_full_name() or reservation.user.username} ({reservation.user.email})\n"
        f"Facility: {reservation.facility.name}\n"
        f"Check-in: {reservation.check_in}\n"
        f"Check-out: {reservation.check_out}\n"
        f"Guests: {reservation.guests}\n"
        f"Total Price: PHP {reservation.total_price}\n"
        f"Status: {reservation.get_status_display()}\n\n"
        f"Please check your Django Admin dashboard for more details."
    )
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER], # Admin receives it
            fail_silently=True,
        )
    except Exception as e:
        logger.error(f"Failed to send booking creation email to admin: {e}")


def notify_admin_payment_success(reservation, payment):
    """Notify the admin when a reservation is successfully paid."""
    if not settings.EMAIL_HOST_USER:
        return

    subject = f"[Payment Received] Reservation #{reservation.pk} has been PAID"
    message = (
        f"A payment has been successfully processed.\n\n"
        f"Reservation ID: #{reservation.pk}\n"
        f"User: {reservation.user.get_full_name() or reservation.user.username} ({reservation.user.email})\n"
        f"Facility: {reservation.facility.name}\n"
        f"Amount Paid: PHP {payment.amount}\n"
        f"Receipt / Payment ID: {payment.receipt_number or payment.paymongo_checkout_id or 'N/A'}\n"
        f"Date Paid: {payment.paid_at}\n\n"
        f"This reservation is now confirmed."
    )
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=True,
        )
    except Exception as e:
        logger.error(f"Failed to send payment success email to admin: {e}")
