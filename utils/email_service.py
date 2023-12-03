from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.conf import settings
from django.template.loader import render_to_string


def send_email(subject, to, context, template):
    try:
        html_message = render_to_string(template, context)
        plain_message = strip_tags(html_message)
        email_account = ''
        send_mail(subject, plain_message, email_account, [to], html_message)
    except:
        pass
