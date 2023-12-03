from django.db import models
from account_module.models import User
from jalali_date import datetime2jalali, date2jalali


#---------------------------------------------------------------------
# a model for article-categories in db
class ArticleCategory(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    parent_category = models.ForeignKey(
        'ArticleCategory',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='دسته بندی والد'
    )
    title = models.CharField(max_length=100, verbose_name='نام')
    url_title = models.CharField(max_length=100, unique=True, verbose_name='عنوان در url')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی مقالات'
        verbose_name_plural = 'دسته بندی های مقالات'


#---------------------------------------------------------------------
# a model for articles in db
class Articles(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    categories = models.ManyToManyField(ArticleCategory, verbose_name='دسته بندی ها')
    title = models.CharField(max_length=100, verbose_name='عنوان')
    image = models.ImageField(upload_to='images/articles', verbose_name='تصویر')
    slug = models.SlugField(
        max_length=200,
        db_index=True,
        allow_unicode=True,
        unique=True,
        verbose_name='عنوان در url'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name='نویسنده',
        editable=False,
        null=True
    )
    created_date = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='تاریخ ایجاد')
    description = models.TextField(verbose_name='توضیحات')
    text = models.TextField(verbose_name='متن مقاله')

    def get_jalali_date(self):
        return date2jalali(self.created_date)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'


#---------------------------------------------------------------------
# a model for comments in db
class ArticleComments(models.Model):
    is_active = models.BooleanField(default=False, verbose_name='نمایش')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, verbose_name='مقاله')
    parent = models.ForeignKey('ArticleComments',null=True, blank=True, on_delete=models.CASCADE, verbose_name='کامنت والد')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    text = models.TextField(verbose_name='متن کامنت')

    def __str__(self):
        return f'({self.article} - {self.user})'

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
