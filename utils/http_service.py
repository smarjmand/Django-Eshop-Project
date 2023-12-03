from django.http import HttpRequest


# ----------------------------------------
# to get client ip :


def get_client_ip(request: HttpRequest):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.splite(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
