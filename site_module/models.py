from django.db import models


# ------------------------------------------------------------------------
# to save site-info in db
class SiteSettings(models.Model):
    is_main_settings = models.BooleanField(default=False, verbose_name='تنظیمات اصلی')
    site_name = models.CharField(max_length=100, verbose_name='نام سایت')
    site_url = models.URLField(max_length=500, verbose_name='دامنه سایت')
    phone_number = models.IntegerField(null=True, blank=True, verbose_name='شماره تماس')
    email = models.EmailField(null=True, blank=True, verbose_name='ایمیل')
    address = models.CharField(max_length=300, null=True, blank=True, verbose_name='آدرس')
    logo = models.ImageField(null=True, blank=True, upload_to='images/site', verbose_name='لوگو سایت')
    about_us = models.TextField(null=True, blank=True, verbose_name='درباره ما')

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = 'تنظیمات'
        verbose_name_plural = 'تنظیمات'


# ------------------------------------------------------------------------
# to save useful websites-categories in db

class FooterLinkCategories(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی لینک ها'
        verbose_name_plural = 'دسته بندی های لینک ها'


# ------------------------------------------------------------------------
# to save useful websites in db

class FooterLinks(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان سایت')
    url = models.URLField(max_length=500, verbose_name='لینک')
    footer_link_category = models.ForeignKey(FooterLinkCategories, on_delete=models.CASCADE, verbose_name='دسته بندی')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'لینک'
        verbose_name_plural = 'لینک ها'


# ------------------------------------------------------------------------
# slider in db

class Slider(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    title = models.CharField(max_length=100, verbose_name='عنوان')
    url = models.URLField(max_length=500, verbose_name='لینک')
    url_title = models.CharField(max_length=100, verbose_name='عنوان لینک')
    image = models.ImageField(upload_to='images/slider', verbose_name='تصویر')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات اسلایدر')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدر ها'


# ------------------------------------------------------------------------
# banners in db


class SiteBanners(models.Model):

    class SiteBannerPositions(models.TextChoices):
        index_page = 'index_page', 'صفحه اصلی'
        products_page = 'products_page', 'صفحه محصولات'
        product_detail_page = 'product_detail_page', 'صفحه جزنیات محصول'
        articles_page = 'articles_page', 'صفحه مقالات'
        article_detail_page = 'article_detail_page', 'صفحه جزئیات مقاله'
        contact_us_page = 'contact_us_page', 'صفحه تماس باما'
        about_us_page = 'about_us_page', 'صفحه درباره ما'

    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_deleted = models.BooleanField(default=False, verbose_name='حذف')
    title = models.CharField(max_length=100, verbose_name='عنوان بنر')
    url = models.URLField(max_length=500, null=True, blank=True, verbose_name='لینک بنر')
    image = models.ImageField(upload_to='images/banners', verbose_name='تصویر')
    position = models.CharField(max_length=200, choices=SiteBannerPositions.choices, verbose_name='جایگاه نمایشی')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'بنر تبلیغاتی'
        verbose_name_plural = 'بنر های تبلیغاتی'
