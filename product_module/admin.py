from django.contrib import admin
from . import models


class ProductsAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'price', 'is_active', 'is_deleted', 'short_description', 'slug']
    list_editable = ['is_active', 'is_deleted']
    list_filter = ['category']
    prepopulated_fields = {
        'slug': ['title']
    }


class ProductCategoriesAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent_category', 'url_title', 'is_active', 'is_deleted']
    list_editable = ['is_active', 'is_deleted', 'parent_category']


class ProductBrandsAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_title', 'is_active', 'is_deleted']
    list_editable = ['is_active', 'is_deleted']


admin.site.register(models.Products, ProductsAdmin)
admin.site.register(models.ProductCategory, ProductCategoriesAdmin)
admin.site.register(models.ProductBrand, ProductBrandsAdmin)
admin.site.register(models.ProductTag)
admin.site.register(models.ProductVisits)
admin.site.register(models.ProductGallery)
