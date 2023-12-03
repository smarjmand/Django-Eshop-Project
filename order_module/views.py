from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from product_module.models import Products
from order_module.models import Order, OrderDetail
from django.contrib.auth.decorators import login_required
from django.conf import settings
import requests
import json


#----------------------------------------------------------------
# a function to add a product to order-basket :
@login_required
def add_product_to_basket(request):
    product_id = request.GET.get('product_id')
    product_count = int(request.GET.get('count'))
    if product_count < 1:
        return JsonResponse({
            'status': 'invalid_count',
            'text': 'تعداد وارد شده صحیح نمی باشد',
            'icon': 'error',
            'confirm_button_text': 'متوجه شدم'
        })
    if request.user.is_authenticated:
        product = (Products.objects.filter(
            id=product_id,
            is_active=True,
            is_deleted=False
        ).first())
        if product is not None:
            current_order, created = Order.objects.get_or_create(
                is_paid=False,
                user_id=request.user.id
            )
            current_order_detail: OrderDetail = current_order.orderdetail_set.filter(
                product_id=product_id,
            ).first()
            if current_order_detail is not None:
                current_order_detail.count += product_count
                current_order_detail.save()
            else:
                OrderDetail.objects.create(
                    order=current_order,
                    product_id=product_id,
                    count=product_count
                )
            return JsonResponse({
                'status': 'success',
                'text': 'مصحول با موفقیت به سبد خرید شما اضافه شد',
                'icon': 'success',
                'confirm_button_text': 'متوجه شدم'
            })
        return JsonResponse({
            'status': 'not_found',
            'text': 'محصول مورد نظر یافت نشد',
            'icon': 'error',
            'confirm_button_text': 'متوجه شدم'
        })
    return JsonResponse({
        'status': 'not_auth',
        'text': 'ابتدا به حساب کاربری خود وارد شوید',
        'icon': 'warning',
        'confirm_button_text': 'متوجه شدم'
    })


#----------------------------------------------------------------
# user basket :
@login_required
def user_basket(request):
    current_order: Order = (
        Order.objects.prefetch_related('orderdetail_set').
        filter(is_paid=False, user_id=request.user.id).first()
    )
    total_price = current_order.get_total_price()
    context = {'order': current_order, 'total_price': total_price}
    return render(request, 'user_basket.html', context)


#----------------------------------------------------------------
# remove an item from basket :
@login_required
def remove_item_from_basket(request):
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'not_found_detail_id'
        })
    deleted_count, deleted_dic = OrderDetail.objects.filter(
        id=detail_id, order__user_id=request.user.id, order__is_paid=False
    ).delete()
    if deleted_count == 0:
        return JsonResponse({
            'status': 'item_not_found'
        })
    current_order: Order = (
        Order.objects.prefetch_related('orderdetail_set').
        filter(is_paid=False, user_id=request.user.id).first()
    )
    total_price = current_order.get_total_price()
    context = {'order': current_order, 'total_price': total_price}
    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_basket_content.html', context)
    })


#----------------------------------------------------------------
# to change number of an item in basket :
@login_required
def change_item_count(request):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if detail_id is None or state is None:
        return JsonResponse({
            'status': 'not_found_detail_id_or_state'
        })
    item: OrderDetail = OrderDetail.objects.filter(
        id=detail_id,
        order__user_id=request.user.id,
        order__is_paid=False
    ).first()
    if item is None:
        return JsonResponse({
            'status': 'item_not_found'
        })
    if state == 'increase':
        item.count += 1
        item.save()
    elif state == 'decrease':
        if item.count == 1:
            item.delete()
        else:
            item.count -= 1
            item.save()
    else:
        return JsonResponse({
            'status': 'invalid_state'
        })
    current_order: Order = (
        Order.objects.prefetch_related('orderdetail_set').
        filter(is_paid=False, user_id=request.user.id).first()
    )
    total_price = current_order.get_total_price()
    context = {'order': current_order, 'total_price': total_price}
    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_basket_content.html', context)
    })


#----------------------------------------------------------------
# zarrin-pal payment request :

#? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

description = "نهایی کردن خرید"
CallbackURL = 'http://127.0.0.1:8000/order/payment-verification'


@login_required
def payment_request(request):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.get_total_price() * 10
    if total_price == 0:
        return redirect('user_basket_page')
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": total_price,
        "Description": description,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
                        'authority': response['Authority']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


#----------------------------------------------------------------
# zarrin-pal payment verification :
@login_required
def payment_verification(request, authority):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.get_total_price() * 10
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": total_price,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            return {'status': True, 'RefID': response['RefID']}
        else:
            return {'status': False, 'code': str(response['Status'])}
    return response
