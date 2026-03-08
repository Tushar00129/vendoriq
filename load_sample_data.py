"""
Sample Data Script for VendorIQ
Run this in Django shell: python manage.py shell < load_sample_data.py

Or manually add vendors through the web interface.
"""

from vendor.models import Vendor

# Sample vendors data
sample_vendors = [
    {
        'name': 'TechSupply Co',
        'delivery_rating': 4.5,
        'quality_rating': 4.8,
        'price_rating': 4.2,
        'communication_rating': 4.6,
    },
    {
        'name': 'Global Materials Ltd',
        'delivery_rating': 3.9,
        'quality_rating': 4.1,
        'price_rating': 4.5,
        'communication_rating': 3.8,
    },
    {
        'name': 'Premium Parts Inc',
        'delivery_rating': 5.0,
        'quality_rating': 4.9,
        'price_rating': 3.5,
        'communication_rating': 4.8,
    },
    {
        'name': 'Budget Components LLC',
        'delivery_rating': 3.5,
        'quality_rating': 3.2,
        'price_rating': 4.9,
        'communication_rating': 3.4,
    },
    {
        'name': 'Elite Manufacturing',
        'delivery_rating': 4.7,
        'quality_rating': 4.9,
        'price_rating': 4.0,
        'communication_rating': 4.9,
    },
    {
        'name': 'Express Logistics',
        'delivery_rating': 4.9,
        'quality_rating': 4.0,
        'price_rating': 4.1,
        'communication_rating': 4.5,
    },
]

# Clear existing vendors (optional)
# Vendor.objects.all().delete()

# Create vendors
created_count = 0
for vendor_data in sample_vendors:
    vendor, created = Vendor.objects.get_or_create(
        name=vendor_data['name'],
        defaults={
            'delivery_rating': vendor_data['delivery_rating'],
            'quality_rating': vendor_data['quality_rating'],
            'price_rating': vendor_data['price_rating'],
            'communication_rating': vendor_data['communication_rating'],
        }
    )
    if created:
        created_count += 1
        print(f"✅ Created: {vendor.name} (Score: {vendor.vendor_score()})")
    else:
        print(f"⏭️  Skipped: {vendor.name} (Already exists)")

print(f"\n📊 Total new vendors created: {created_count}")
print(f"📊 Total vendors in database: {Vendor.objects.count()}")
