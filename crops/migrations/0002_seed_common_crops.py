from django.db import migrations


CROPS = [
    ('Rice', 'CEREALS'),
    ('Wheat', 'CEREALS'),
    ('Maize', 'CEREALS'),
    ('Chickpea', 'PULSES'),
    ('Tomato', 'VEGETABLES'),
    ('Onion', 'VEGETABLES'),
    ('Potato', 'VEGETABLES'),
    ('Green Chilli', 'VEGETABLES'),
    ('Banana', 'FRUITS'),
    ('Mango', 'FRUITS'),
    ('Groundnut', 'OILSEEDS'),
    ('Mustard', 'OILSEEDS'),
]


def add_common_crops(apps, schema_editor):
    Crop = apps.get_model('crops', 'Crop')
    Crop.objects.using(schema_editor.connection.alias).bulk_create(
        [Crop(name=name, category=category) for name, category in CROPS],
        ignore_conflicts=True,
    )


def remove_common_crops(apps, schema_editor):
    Crop = apps.get_model('crops', 'Crop')
    Crop.objects.using(schema_editor.connection.alias).filter(
        name__in=[name for name, _ in CROPS],
        listings__isnull=True,
    ).delete()


class Migration(migrations.Migration):
    dependencies = [('crops', '0001_initial')]

    operations = [migrations.RunPython(add_common_crops, remove_common_crops)]
