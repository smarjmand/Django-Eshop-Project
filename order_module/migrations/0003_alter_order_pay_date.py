# Generated by Django 4.2.7 on 2023-11-28 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_module', '0002_alter_order_options_alter_orderdetail_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pay_date',
            field=models.DateField(blank=True, null=True, verbose_name='زمان و تاریخ پرداخت'),
        ),
    ]
