from django.urls import path
from . import views


urlpatterns = [
    path('add-product-to-basket', views.add_product_to_basket, name='add_product_to_basket_view'),
    path('user-basket', views.user_basket, name='user_basket_page'),
    path('remove-product-from-basket', views.remove_item_from_basket, name='remove_item_from_basket_view'),
    path('change-item-count', views.change_item_count, name='change_item_count_view'),
    path('payment-request', views.payment_request, name='payment_request_view'),
    path('payment-verification', views.payment_verification, name='payment_verification_view'),
]
