from django.db import models
from product_module.models import Products
from account_module.models import User


#----------------------------------------------------------------
# model for Order ( Purchase registration ) :
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(verbose_name='نهایی شده')
    pay_date = models.DateTimeField(null=True, blank=True, verbose_name='زمان و تاریخ پرداخت')

    def get_total_price(self):
        total_price = 0
        for order_detail in self.orderdetail_set.all():
            total_price += (order_detail.product.price * order_detail.count)
        return total_price

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'سبد خرید کاربر'
        verbose_name_plural = 'سبد های خرید کاربران'


#----------------------------------------------------------------
# model for Order-Details ( Products in Order ) :
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='کالا')
    count = models.IntegerField(verbose_name='تعداد کالا')

    def get_total_price(self):
        return self.count * self.product.price

    def __str__(self):
        return f'{self.order}/{self.product}/{self.count}'

    class Meta:
        verbose_name = 'آیتم سبد خرید'
        verbose_name_plural = 'کالاهای سبد های خرید کاربران'
