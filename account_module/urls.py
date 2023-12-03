from django.urls import path
from . import views

urlpatterns = [
    path('register', views.RegistrationView.as_view(), name='register_page'),
    path('login', views.LoginView.as_view(), name='login_page'),
    path('logout', views.logout_user, name='logout_user'),
    path('user-panel-dashboard', views.UserPanelDashboardView.as_view(), name='user_panel_page'),
    path('edit-profile', views.EditUserProfileView.as_view(), name='edit_profile_page'),
    path('change-password', views.ChangePassword.as_view(), name='change_password_page'),
    path('forget-password', views.ForgetPasswordView.as_view(), name='forget_password_page'),
    path('acocunt-message/<slug>', views.account_message, name='account_message_page'),
    path('reset-password/<reset_password_code>', views.ResetPasswordView.as_view(), name='reset_password_page'),
    path('activate-account/<activation_code>', views.ActivateAccountView.as_view(), name='activation_page'),
    path('previous-orders', views.PreviousOrders.as_view(), name='previous_orders_page'),
    path('previous-order-detail/<order_id>', views.previous_order_detail, name='previous_order_detail_page'),
]
