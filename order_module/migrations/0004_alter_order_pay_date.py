# Generated by Django 4.2.7 on 2023-11-28 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_module', '0003_alter_order_pay_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pay_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='زمان و تاریخ پرداخت'),
        ),
    ]
