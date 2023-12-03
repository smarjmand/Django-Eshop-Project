from django.contrib import admin
from .models import ContactUs

# Register your models here.


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['subject', 'is_read_by_admin', 'email']


admin.site.register(ContactUs, ContactUsAdmin)
