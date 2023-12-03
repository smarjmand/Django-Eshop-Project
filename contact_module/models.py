from django.db import models


class ContactUs(models.Model):
    subject = models.CharField(max_length=100, verbose_name='موضوع')
    email = models.EmailField(max_length=100, verbose_name='ایمیل')
    name = models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')
    message = models.TextField(verbose_name='متن پیام')
    is_read_by_admin = models.BooleanField(verbose_name='خوانده شده', default=False)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    response = models.TextField(verbose_name='پاسخ', null=True, blank=True)

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'

    def __str__(self):
        return self.subject


class UserProfile(models.Model):
    # image = models.FileField(upload_to='profile_images')
    image = models.ImageField(upload_to='profile_images')
