from django.db import models
from django.conf import settings
from reservations.models import Reservation


class Payment(models.Model):
    """
    Payment transaction record (D4 in SRS).
    Implements Process 3.0 — Payment Processing.
    """

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        PAID = 'paid', 'Paid'
        FAILED = 'failed', 'Failed'
        REFUNDED = 'refunded', 'Refunded'

    class PaymentMethod(models.TextChoices):
        GCASH = 'gcash', 'GCash'
        MAYA = 'maya', 'Maya'
        CARD = 'card', 'Credit/Debit Card'

    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name='payments',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    # PayMongo reference fields
    paymongo_checkout_id = models.CharField(max_length=255, blank=True)
    paymongo_payment_id = models.CharField(max_length=255, blank=True)
    checkout_url = models.URLField(blank=True)
    # Receipt
    receipt_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment #{self.pk} — ₱{self.amount} ({self.get_status_display()})"

    def generate_receipt_number(self):
        """Generate a unique receipt number."""
        import uuid
        self.receipt_number = f"JPR-{uuid.uuid4().hex[:8].upper()}"
        return self.receipt_number
