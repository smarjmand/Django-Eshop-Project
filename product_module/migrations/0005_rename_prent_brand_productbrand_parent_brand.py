# Generated by Django 4.2.4 on 2023-10-14 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0004_productbrand_prent_brand'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productbrand',
            old_name='prent_brand',
            new_name='parent_brand',
        ),
    ]
