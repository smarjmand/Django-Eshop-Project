# Generated by Django 4.2.4 on 2023-08-21 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0003_alter_user_email_active_code_alter_user_mobile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='mobile',
        ),
    ]
