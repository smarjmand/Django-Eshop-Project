from django.urls import path
from . import views

urlpatterns = [
        # to use function-based view :
    # path('', views.products_list, name='products_page'),
    # path('<data>', views.product_detail, name='product_detail_page'),
    #---------------------------------------------------------------------
        # to use class based view :
    path('', views.ProductListView.as_view(), name='products_page'),
    path('cat/<product_category>', views.ProductListView.as_view(), name='products_by_category_page'),
    path('brand/<product_brand>', views.ProductListView.as_view(), name='products_by_brand_page'),
    path('<slug>', views.ProductDetailView.as_view(), name='product_detail_page'),
]
