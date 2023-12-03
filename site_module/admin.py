from django.contrib import admin
from .models import SiteSettings, FooterLinkCategories, FooterLinks, Slider, SiteBanners


class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'site_url', 'is_main_settings']
    list_editable = ['is_main_settings']


class FooterLinksAdmin(admin.ModelAdmin):
    list_display = ['title', 'footer_link_category', 'url']
    list_editable = ['footer_link_category']


class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'is_active']
    list_editable = ['is_active']


class SiteBannersAdmin(admin.ModelAdmin):
    list_display = ['title', 'position', 'is_active', 'is_deleted']
    list_editable = ['position', 'is_active', 'is_deleted']


# Register your models here.
admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(FooterLinkCategories)
admin.site.register(FooterLinks, FooterLinksAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(SiteBanners, SiteBannersAdmin)
