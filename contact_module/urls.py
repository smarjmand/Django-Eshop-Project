from django.urls import path
from . import views

urlpatterns = [
        # for function-base views :
    # path('', views.contact_page, name='contact_page')
    #----------------------------------------------------------------------
        # for class-based views :
    path('', views.ContactPageView.as_view(), name='contact_page'),
    path('create-profile', views.CreateProfileView.as_view(), name='create_profile_page'),
    path('profiles', views.ProfileListView.as_view(), name='profiles_page')
]