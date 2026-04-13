import os
import sys
import django

# Add project root to path
sys.path.append(os.getcwd())

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core.models import RatePackage

def add_rates():
    rates_to_add = [
        {
            "name": "DAY TOUR RATE",
            "price": 7000,
            "inclusions": "One Adult Pool & One Kiddie size Pool\nCottages\n2 pcs of 6ft Long tables\nVolleyball Court\nCamp Fire\nWI-FI\nSwing",
            "note": "Heavy Duty Gas Griller (PHP 200)",
            "order": 1
        },
        {
            "name": "NIGHT TOUR RATE",
            "price": 9000,
            "inclusions": "One Adult Pool & One Kiddie size Pool\nCottages\n2 pcs of 6ft Long tables\nVolleyball Court\nCamp Fire\nWI-FI\nSwing",
            "note": "Heavy Duty Gas Griller (PHP 200)",
            "order": 2
        },
        {
            "name": "EVENT RATE",
            "price": 20000,
            "inclusions": "MULTIFUNCTIONAL HALL\nADULT & KID SIZE POOL\n4 pcs of 6ft Long Tables\n4 pcs of Round Tables\n50 pcs of Chairs\nKitchen\nCottages\nVolleyball Court\nCamp Fire\nWI-FI\nSwing",
            "note": "",
            "order": 3
        }
    ]

    for rate in rates_to_add:
        pkg, created = RatePackage.objects.get_or_create(
            name=rate["name"],
            defaults={
                "price": rate["price"],
                "inclusions": rate["inclusions"],
                "note": rate["note"],
                "order": rate["order"]
            }
        )
        if created:
            print(f"Added: {rate['name']}")
        else:
            pkg.price = rate["price"]
            pkg.inclusions = rate["inclusions"]
            pkg.note = rate["note"]
            pkg.order = rate["order"]
            pkg.save()
            print(f"Updated: {rate['name']}")

if __name__ == "__main__":
    add_rates()
