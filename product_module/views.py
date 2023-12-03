from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Products, ProductCategory, ProductBrand, ProductVisits, ProductGallery
from site_module.models import SiteBanners
from django.views.generic import ListView, DetailView
from utils.http_service import get_client_ip
from utils.convertors import group_list


#--------------------------------------------------------------
## function-based views :
def products_list(request):
    products = Products.objects.all().order_by('price')
    context = {'products': products}
    return render(request, 'product_list.html', context)


def product_detail(request, data):
    product = get_object_or_404(Products, slug=data)
    # return HttpResponse(render_to_string('product_detail.html', {'product': product}))
    return render(request, 'product_detail.html', {'product': product})


def product_categories_component(request):
    categories: ProductCategory = ProductCategory.objects.prefetch_related('productcategory_set').filter(is_active=True, is_deleted=False, parent_category=None)
    return render(request, 'components/product_categories_component.html', {'categories': categories})


def product_brands_component(request):
    brands: ProductBrand = ProductBrand.objects.annotate(products_count=Count('products')).filter(is_deleted=False, is_active=True)
    return render(request, 'components/product_brands_components.html', {'brands': brands})


#--------------------------------------------------------------
## class-based views :
class ProductListView(ListView):
    template_name = 'product_list.html'
    model = Products
    context_object_name = 'products'
    ordering = ['price']
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        product: Products = Products.objects.order_by('-price').first()
        db_max_price = product.price if product is not None else 0
        context['max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or db_max_price
        context['banners'] = SiteBanners.objects.filter(
            is_active=True,
            is_deleted=False,
            position__iexact=SiteBanners.SiteBannerPositions.products_page
        )
        return context

    def get_queryset(self):
        base_query = super(ProductListView, self).get_queryset()
        category_name = self.kwargs.get('product_category')
        brand_name = self.kwargs.get('product_brand')
        data = base_query.filter(is_deleted=False, is_active=True)
        start_price = self.request.GET.get('start_price')
        end_price = self.request.GET.get('end_price')
        if start_price is not None:
            data = data.filter(price__gte=start_price)
        if end_price is not None:
            data = data.filter(price__lte=end_price)
        if category_name is not None:
            data = data.filter(category__url_title__iexact=category_name)
        elif brand_name is not None:
            data = data.filter(brand__url_title__iexact=brand_name)
        return data


class ProductDetailView(DetailView):
    template_name = 'product_detail.html'
    model = Products
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # get banners from db : ------------------------------
        context['banners'] = SiteBanners.objects.filter(
            is_active=True,
            is_deleted=False,
            position__iexact=SiteBanners.SiteBannerPositions.product_detail_page
        )
        # save product-visits in db : ------------------------
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        has_been_visited = ProductVisits.objects.filter(ip__iexact=user_ip, product_id=self.object.id).exists()
        if not has_been_visited:
            ProductVisits.objects.create(
                ip=user_ip,
                product_id=self.object.id,
                user_id=user_id or None
            )
        # get product-images from db : -----------------------
        product_images = list(ProductGallery.objects.filter(product_id=self.object.id))
        product_images.append(self.object)
        context['product_gallery'] = group_list(product_images, 3)
        # get products by brand from db : --------------------
        context['related_products'] = group_list(Products.objects.filter(brand_id=self.object.brand_id).exclude(pk=self.object.id).all()[:12], 3)
        return context
