from django.db import models


class RatePackage(models.Model):
    """
    A bookable rate package (e.g. Day Tour, Night Tour, Event).
    Admin can upload a photo and edit prices from the Django admin panel.
    """

    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in PHP")
    inclusions = models.TextField(
        help_text="One inclusion per line. e.g.:\nAdult Pool & Kiddie Pool\nCottages"
    )
    note = models.CharField(
        max_length=300,
        blank=True,
        help_text="Optional note shown below inclusions (e.g. Gas Griller add-on)"
    )
    photo = models.ImageField(
        upload_to='rates/',
        blank=True,
        null=True,
        help_text="Optional banner/header photo for this package"
    )
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower = first)")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Rate Package'
        verbose_name_plural = 'Rate Packages'

    def __str__(self):
        return f"{self.name} — ₱{self.price:,.0f}"

    def inclusions_list(self):
        """Return inclusions as a list of stripped lines."""
        return [line.strip() for line in self.inclusions.splitlines() if line.strip()]


# Create your models here.
