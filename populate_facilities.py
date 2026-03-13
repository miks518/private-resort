from facilities.models import Facility
from django.utils.text import slugify

facilities_data = [
    {
        "name": "Grand Infinity Pool",
        "description": "A stunning infinity pool overlooking the resort with crystal clear waters.",
        "capacity": 50,
        "price_per_day": 5000,
        "map_x": 50,
        "map_y": 40
    },
    {
        "name": "Luxury Villa Alpha",
        "description": "Private villa with premium amenities and a view of the garden.",
        "capacity": 6,
        "price_per_day": 12000,
        "map_x": 30,
        "map_y": 60
    },
    {
        "name": "Tropical Garden Cafe",
        "description": "Al-fresco dining experience surrounded by lush tropical plants.",
        "capacity": 30,
        "price_per_day": 2000,
        "map_x": 70,
        "map_y": 65
    },
    {
        "name": "Zen Spa & Wellness",
        "description": "Relax and rejuvenate with our signature spa treatments.",
        "capacity": 10,
        "price_per_day": 3500,
        "map_x": 20,
        "map_y": 25
    },
    {
        "name": "Sunset Deck",
        "description": "The perfect spot to watch the sun go down with a refreshing drink.",
        "capacity": 20,
        "price_per_day": 1500,
        "map_x": 80,
        "map_y": 30
    }
]

for data in facilities_data:
    facility, created = Facility.objects.get_or_create(
        slug=slugify(data["name"]),
        defaults=data
    )
    if not created:
        for key, value in data.items():
            setattr(facility, key, value)
        facility.save()
    print(f"{'Created' if created else 'Updated'} {facility.name}")
