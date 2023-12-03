from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser


#----------------------------------------------------------------
# model for user :
class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/profile',null=True, blank=True, verbose_name='تصویر کاربر')
    email_active_code = models.CharField(max_length=100, verbose_name='کد فعال سازی ایمیل')
    email_active_code_time = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    address = models.TextField(null=True, blank=True, verbose_name='آدرس کاربر')
    about_user = models.TextField(null=True, blank=True, verbose_name='درباره کاربر')

    def __str__(self):
        if (self.first_name and self.last_name) != '':
            return self.get_full_name()
        return self.username

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'


#----------------------------------------------------------------
# model for registration-messages :
class RegisterMessages(models.Model):
    title = models.CharField(max_length=200, verbose_name='نوع پیام')
    text = models.CharField(max_length=500, verbose_name='متن پیام')
    image = models.ImageField(upload_to='images/messages', null=True, blank=True, verbose_name='تصویر پیام')
    slug = models.SlugField(max_length=100, unique=True, null=False, db_index=True, verbose_name='اسلاگ')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'اختار حساب کاربری'
        verbose_name_plural = 'اختار های حساب کاربری'
