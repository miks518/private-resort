from django.db import migrations

def add_official_rates(apps, schema_editor):
    RatePackage = apps.get_model('core', 'RatePackage')
    
    # Clear existing packages if any (to avoid duplicates during deployment)
    RatePackage.objects.all().delete()
    
    # Official Rates Data
    RatePackage.objects.create(
        name="DAY TOUR RATE",
        price=7000,
        inclusions="One Adult Pool & One Kiddie size Pool\nCottages\n2 pcs of 6ft Long tables\nVolleyball Court\nCamp Fire\nWI-FI\nSwing\nHeavy Duty Gas Griller (PHP 200)",
        note="Standard day tour access.",
        order=1
    )
    
    RatePackage.objects.create(
        name="NIGHT TOUR RATE",
        price=9000,
        inclusions="One Adult Pool & One Kiddie size Pool\nCottages\n2 pcs of 6ft Long tables\nVolleyball Court\nCamp Fire\nWI-FI\nSwing\nHeavy Duty Gas Griller (PHP 200)",
        note="Late night relaxation and swimming.",
        order=2
    )
    
    RatePackage.objects.create(
        name="EVENT RATE",
        price=20000,
        inclusions="MULTIFUNCTIONAL HALL\nADULT & KID SIZE POOL\n4 pcs of 6ft Long Tables\n4 pcs of Round Tables\n50 pcs of Chairs\nKitchen\nCottages\nVolleyball Court\nCamp Fire\nWI-FI\nSwing",
        note="Perfect for birthdays, weddings, and reunions.",
        order=3
    )

def remove_official_rates(apps, schema_editor):
    RatePackage = apps.get_model('core', 'RatePackage')
    RatePackage.objects.filter(name__in=["DAY TOUR RATE", "NIGHT TOUR RATE", "EVENT RATE"]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_official_rates, remove_official_rates),
    ]
