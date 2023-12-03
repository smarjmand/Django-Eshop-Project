from django.shortcuts import render
from django.views.generic import TemplateView
from site_module.models import SiteSettings, FooterLinkCategories, Slider
from product_module.models import Products, ProductCategory
from utils.convertors import group_list
from django.db.models import Count, Sum

#-------------------------------------------------------------
## to load header and footer by django_render_partial :


def site_header_component(request):
    setting: SiteSettings = SiteSettings.objects.filter(is_main_settings=True).first()
    context = {'setting': setting}
    return render(request, 'shared/site_header_component.html', context)


def site_footer_component(request):
    setting: SiteSettings = SiteSettings.objects.filter(is_main_settings=True).first()
    links_categories: FooterLinkCategories = FooterLinkCategories.objects.all()
    context = {'setting': setting, 'links_categories': links_categories}
    return render(request, 'shared/site_footer_component.html', context)


#-------------------------------------------------------------
## to load index page (function-based view):
'''def index_page(request):
    return render(request, 'index.html')'''


#-------------------------------------------------------------
## to load index page by TemplateView (class-based view):
class IndexPageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        sliders: Slider = Slider.objects.filter(is_active=True)
        context['sliders'] = sliders
        # get latest-products from db : --------------------------
        latest_products = Products.objects.filter(is_deleted=False, is_active=True).order_by('-created_date')[:12]
        context['latest_products'] = group_list(latest_products, 4)
        # get most-visited-products from db : --------------------
        most_visited_products = Products.objects.filter(is_active=True, is_deleted=False).annotate(visits_count=Count('productvisits')).order_by('-visits_count')[:12]
        context['most_visited_products'] = group_list(most_visited_products, 4)
        # get product-categories from db : -----------------------
        categories = list(ProductCategory.objects.annotate(products_count=Count('products')).filter(is_active=True, is_deleted=False, products_count__gt=0)[:5])
        product_categories = []
        for category in categories:
            item = {
                'id': category.id,
                'title': category.title,
                'products': category.products_set.all()[:4]
            }
            product_categories.append(item)
        context['products_categories'] = product_categories
        # get most bought items from db : ------------------------
        most_bought_products = (
            Products.objects.filter(orderdetail__order__is_paid=True)
            .annotate(order_count=Sum('orderdetail__count')).order_by('-order_count')
        )
        context['most_bought_products'] = group_list(most_bought_products[:12], 4)
        return context


#-------------------------------------------------------------
## to load about-us page (class-based view) :
class AboutPageView(TemplateView):
    template_name = 'about-us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        settings: SiteSettings = SiteSettings.objects.filter(is_main_settings=True).first()
        context['settings'] = settings
        return context
