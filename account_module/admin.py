from django.contrib import admin
from .models import User, RegisterMessages


class RegisterMessagesAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['title']
    }


# Register your models here.
admin.site.register(User)
admin.site.register(RegisterMessages, RegisterMessagesAdmin)
