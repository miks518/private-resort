from django.db import models


class Facility(models.Model):
    """
    Represents a bookable facility at the resort.
    """

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    capacity = models.PositiveIntegerField(help_text="Maximum number of guests")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='facilities/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Facilities'
        ordering = ['name']

    def __str__(self):
        return self.name


class FacilityImage(models.Model):
    """Additional gallery images for a facility."""

    facility = models.ForeignKey(
        Facility, on_delete=models.CASCADE, related_name='gallery_images'
    )
    image = models.ImageField(upload_to='facilities/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.facility.name} — Image {self.order}"


class VirtualTour(models.Model):
    """
    Virtual tour media associated with a facility.
    """

    class MediaType(models.TextChoices):
        IMAGE = 'image', 'Image'
        VIDEO = 'video', 'Video'
        PANORAMA = 'panorama', '360° Panorama'

    facility = models.ForeignKey(
        Facility, on_delete=models.CASCADE, related_name='virtual_tours'
    )
    title = models.CharField(max_length=200)
    media_type = models.CharField(max_length=20, choices=MediaType.choices)
    media_file = models.FileField(upload_to='virtual_tours/')
    thumbnail = models.ImageField(upload_to='virtual_tours/thumbs/', blank=True, null=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.get_media_type_display()})"
