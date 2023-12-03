from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from account_module.models import User


#----------------------------------------------------------------------
# model for products' categories
class ProductCategory(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_deleted = models.BooleanField(default=False, verbose_name='حذف شده')
    parent_category = models.ForeignKey(
        "ProductCategory",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='دسته بندی والد'
    )
    title = models.CharField(max_length=100, verbose_name='عنوان', db_index=True)
    url_title = models.CharField(max_length=100, verbose_name='عنوان در url', db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی محصولات'
        verbose_name_plural = 'دسته بندی های محصولات'


#----------------------------------------------------------------------
# model for products' brand :
class ProductBrand(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_deleted = models.BooleanField(default=False, verbose_name='حذف')
    title = models.CharField(max_length=100, db_index=True, verbose_name='برند محصول')
    url_title = models.CharField(max_length=100,db_index=True, verbose_name='عنوان در url')

    class Meta:
        verbose_name = 'برند محصولات'
        verbose_name_plural = 'برند های محصولات'

    def __str__(self):
        return self.title


#----------------------------------------------------------------------
# model for products :
class Products(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='عنوان'
    )
    price = models.IntegerField(verbose_name='قیمت')
    image = models.ImageField(
        upload_to='products',
        blank=True,
        null=True,
        verbose_name=
        'تصویر محصول'
    )
    category = models.ManyToManyField(
        ProductCategory,
        verbose_name='دسته بندی ها'
    )
    brand = models.ForeignKey(
        ProductBrand,
        on_delete=models.CASCADE,
        verbose_name='برند',
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال'
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name='حذف شده'
    )
    short_description = models.CharField(
        max_length=200,
        null=True,
        verbose_name='خلاصه توضیحات',
        db_index=True
    )
    description = models.TextField(verbose_name='توضیحات', db_index=True)
    slug = models.SlugField(
        default='',
        null=False,
        verbose_name='اسلاگ',
        max_length=200,
        unique=True,
        blank=True
    )
    created_date = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='تاریخ ایجاد')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail_page', args=[self.slug])

    def __str__(self):
        return f'{self.title}({self.price})__ID:{self.id}'

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


#----------------------------------------------------------------------
# model for product's tags :
class ProductTag(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان', db_index=True)
    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        verbose_name='محصولات'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'تگ محصول'
        verbose_name_plural = 'تگ های محصولات'


#----------------------------------------------------------------------
# model for products-visits :

class ProductVisits(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='محصول')
    ip = models.CharField(max_length=50, verbose_name='آی پی کاربر')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='کاربر')

    def __str__(self):
        return f'{self.product.title} / {self.ip}'

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدید های محصولات'


#----------------------------------------------------------------------
# model for products-gallery :

class ProductGallery(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='images/product-gallery', verbose_name='تصویر محصول')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'تصویر محصول در گالری'
        verbose_name_plural = 'گالری تصاویر محصولات'