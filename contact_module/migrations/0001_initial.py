# Generated by Django 4.2.4 on 2023-08-21 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100, verbose_name='موضوع')),
                ('email', models.EmailField(max_length=100, verbose_name='ایمیل')),
                ('name', models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')),
                ('message', models.TextField(verbose_name='متن پیام')),
                ('is_read_by_admin', models.BooleanField(default=False, verbose_name='خوانده شده')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('response', models.TextField(blank=True, null=True, verbose_name='پاسخ')),
            ],
            options={
                'verbose_name': 'پیام',
                'verbose_name_plural': 'پیام ها',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='profile_images')),
            ],
        ),
    ]
