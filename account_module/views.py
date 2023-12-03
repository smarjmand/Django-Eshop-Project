from django.shortcuts import render, redirect
from django.views.generic import View,TemplateView, ListView
from .forms import RegisterForm, LoginForm, ForgetPasswordForm, ResetPasswordForm, EditProfileModelForm, ChangePasswordForm
from .models import User, RegisterMessages
from django.utils.crypto import get_random_string
from django.contrib.auth import login, logout
from utils.email_service import send_email
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from order_module.models import Order


#############################################################
# these are middle-wares for account-management ( registration, login, logout, reset-password )
#############################################################


#------------------------------------------------------------
# show messages to user :
    # get message-slug
    # check in db for message and show to user
def account_message(request, slug):
    message = RegisterMessages.objects.filter(slug=slug).first()
    return render(request, 'registrations_message.html', {'message': message})


#------------------------------------------------------------
# registering user :
    # get password & email from user and check if they are valid
    # check if email exists in db and if it doesn't register user
    # send activation code to user's email
class RegistrationView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'registration.html', {'form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST or None)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            user = User.objects.filter(email__iexact=user_email).exists()
            if user:
                register_form.add_error('email', 'این ایمیل قبلا ثبت نام کرده است')
            else:
                new_user = User(
                    email=user_email,
                    email_active_code=get_random_string(72),
                    is_active=False,
                    username=user_email
                )
                new_user.set_password(user_password)
                new_user.save()
                send_email('فعال سازی حساب کاربری', new_user.email, {'user': new_user}, 'emails/activate_account.html')
                return redirect('account_message_page', 'registration')
        return render(request, 'registration.html', {'form': register_form})


#------------------------------------------------------------
# activate account by sent email :
    # check if there is any user with that activation-code
    # check if user's account is active
    # check if activation code is expired, and if it's not, activate account
class ActivateAccountView(View):
    def get(self, request, activation_code):
        user = User.objects.filter(email_active_code__iexact=activation_code).first()
        if user:
            if not user.is_active:
                now_time = timezone.now()
                activation_code_time = user.email_active_code_time
                time_difference = now_time - activation_code_time
                if time_difference.seconds <= 1800:
                    user.is_active = True
                    user.email_active_code = get_random_string(72)
                    user.save()
                    return redirect('account_message_page', 'success-registration')
                else:
                    return redirect('account_message_page', 'expire-registration-code')
            else:
                return redirect('account_message_page', 'account-is-activated')
        return redirect('account_message_page', 'not-found')


#------------------------------------------------------------
# login user :
    # get email and password from user
    # check if user exists in db
    # check if user's account is activated
    # check if password is correct and if it is, login user
class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'login.html', {'form': login_form})

    def post(self, request):
        login_form = LoginForm(request.POST or None)
        if login_form.is_valid():
            input_email = login_form.cleaned_data.get('email')
            input_password = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=input_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'حساب کاربری شما فعال نشده است')
                else:
                    is_correct = user.check_password(input_password)
                    if is_correct:
                        login(request, user)
                        return redirect('index_page')
                    else:
                        login_form.add_error('email', 'کاربری با مشخصات وارد شده یافت نشد')
            else:
                login_form.add_error('email', 'کاربری با مشخصات وارد شده یافت نشد')
        return render(request, 'login.html', {'form': login_form})


#------------------------------------------------------------
# send reset password link to user :
    # get email from user
    # check if email exists in db
    # if user exists, set new activation-code and new activation-code-time
    # send new activation code to user's email
class ForgetPasswordView(View):
    def get(self, request):
        recovery_form = ForgetPasswordForm()
        return render(request, 'forget_password.html', {'form': recovery_form})

    def post(self, request):
        recovery_form = ForgetPasswordForm(request.POST or None)
        if recovery_form.is_valid():
            input_email = recovery_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=input_email).first()
            if user is not None:
                user.email_active_code = get_random_string(72)
                user.email_active_code_time = timezone.now()
                user.save()
                send_email('فراموشی کلمه عبور', user.email, {'user': user}, 'emails/forgot_password.html')
                return redirect('account_message_page', 'forget-password')
            recovery_form.add_error('email', 'کاربری با این مشخصات یافت نشد')
        return render(request, 'forget_password.html', {'form': recovery_form})


#------------------------------------------------------------
# reset password :
    # check if there is any user with that activation-code
    # check if activation-code is expired, if it is, show error
    # get new-password
    # check if new-password is valid, if it is :
        # set new-password
        # set new-activation-code
        # set new-activation-code-time
    # show success message
class ResetPasswordView(View):
    def get(self, request, reset_password_code):
        user: User = User.objects.filter(email_active_code__iexact=reset_password_code).first()
        if user is not None:
            now_time = timezone.now()
            activation_code_time = user.email_active_code_time
            time_difference = now_time - activation_code_time
            if time_difference.seconds <= 1800:
                reset_pass_form = ResetPasswordForm()
                return render(request, 'reset_password.html', {'form': reset_pass_form})
            return redirect('account_message_page', 'expire-registration-code')
        return redirect('account_message_page', 'not-found')

    def post(self, request, reset_password_code):
        reset_pass_form = ResetPasswordForm(request.POST or None)
        user: User = User.objects.filter(email_active_code__iexact=reset_password_code).first()
        if reset_pass_form.is_valid():
            input_password = reset_pass_form.cleaned_data.get('password')
            if user is not None:
                user.set_password(input_password)
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.email_active_code_time = timezone.now()
                user.save()
                return redirect('account_message_page', 'success-reset-password')
            return redirect('account_message_page', 'not-found')
        return render(request, 'reset_password.html', {'form': reset_pass_form})


#------------------------------------------------------------
# logout user :
def logout_user(request):
    logout(request)
    return redirect('index_page')


#############################################################
# these are middle-wares for user-panel ( change password, change user info )
#############################################################


#------------------------------------------------------------
# to load user-panel-dashboard :
@method_decorator(login_required, name='dispatch')
class UserPanelDashboardView(TemplateView):
    template_name = 'user_panel_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        current_user: User = User.objects.filter(id=self.request.user.id).first()
        context['user'] = current_user
        return context


#------------------------------------------------------------
# to load user-panel-menu by render_partial :
def user_panel_menu_component(request):
    return render(request, 'components/user_panel_menu_component.html')


#------------------------------------------------------------
# to edit user-profile :
@method_decorator(login_required, name='dispatch')
class EditUserProfileView(View):
    def get(self, request):
        current_user: User = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(instance=current_user)
        context = {'form': edit_form, 'avatar': current_user.avatar}
        return render(request, 'edit_profile.html', context)

    def post(self, request):
        current_user: User = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(request.POST or None, request.FILES, instance=current_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)
        context = {'form': edit_form, 'avatar': current_user.avatar}
        return render(request, 'edit_profile.html', context)


#------------------------------------------------------------
# to change password :
  # get current-password and new-password from user
  # if current-password is correct, save it
@method_decorator(login_required, name='dispatch')
class ChangePassword(View):
    def get(self, request):
        return render(request, 'change_password.html', {'form': ChangePasswordForm()})

    def post(self, request):
        change_form = ChangePasswordForm(request.POST or None)
        if change_form.is_valid():
            current_user: User = User.objects.filter(id=request.user.id).first()
            current_pass = change_form.cleaned_data.get('current_password')
            new_pass = change_form.cleaned_data.get('new_password')
            if current_user.check_password(current_pass):
                current_user.set_password(new_pass)
                current_user.save()
                logout(request)
                return redirect('login_page')
            change_form.add_error('current_password', 'کلمه عبور وارد شده اشتباه است')
        return render(request, 'change_password.html', {'form': change_form})


#------------------------------------------------------------
# to see previous orders :
@method_decorator(login_required, name='dispatch')
class PreviousOrders(ListView):
    model = Order
    template_name = 'previous_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(user_id=self.request.user.id)
        return query


#------------------------------------------------------------
# to see previous orders detail :
def previous_order_detail(request, order_id):
    order = Order.objects.prefetch_related('orderdetail_set').filter(id=order_id, user_id=request.user.id).first()
    return render(request, 'previous_order_detail.html', {'order': order})





























