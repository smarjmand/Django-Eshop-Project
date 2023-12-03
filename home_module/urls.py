from django.urls import path
from . import views


urlpatterns = [
        # for function based view :
    # path('', views.index_page, name='index_page')
    #---------------------------------------------------------
    path('', views.IndexPageView.as_view(), name='index_page'),
    path('about-us', views.AboutPageView.as_view(), name='about_us_page')
]
