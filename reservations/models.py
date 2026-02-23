from django.db import models
from django.conf import settings
from facilities.models import Facility


class Reservation(models.Model):
    """
    Booking record linking a user to a facility for specific dates (D2 in SRS).
    Implements Process 2.0 — Reservation Management.
    """

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        PAID = 'paid', 'Paid'
        CANCELLED = 'cancelled', 'Cancelled'
        COMPLETED = 'completed', 'Completed'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations',
    )
    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name='reservations',
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    special_requests = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Reservation #{self.pk} — {self.user} @ {self.facility} ({self.check_in} to {self.check_out})"

    def calculate_total(self):
        """Calculate total price based on number of days and facility rate."""
        if self.check_in and self.check_out:
            days = (self.check_out - self.check_in).days
            if days > 0:
                self.total_price = self.facility.price_per_day * days
        return self.total_price

    @property
    def duration_days(self):
        if self.check_in and self.check_out:
            return (self.check_out - self.check_in).days
        return 0
