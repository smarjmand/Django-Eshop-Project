# Generated by Django 4.2.4 on 2023-09-12 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0004_footerlinkcategories_footerlinks'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('url', models.URLField(max_length=500, verbose_name='لینک')),
                ('url_title', models.CharField(max_length=100, verbose_name='عنوان لینک')),
                ('image', models.ImageField(upload_to='images/slider', verbose_name='تصویر')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات اسلایدر')),
            ],
            options={
                'verbose_name': 'اسلایدر',
                'verbose_name_plural': 'اسلایدر ها',
            },
        ),
    ]
