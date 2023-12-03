from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from account_module.models import User


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(),
        max_length=100,
        error_messages={
            'required': 'ایمیل خود را وارد کنید',
            'max_length': 'ایمیل باید حداکثر 100 کاراکتر باشد'
        },
        validators=[validators.EmailValidator]
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(),
        min_length=4,
        max_length=20,
        error_messages={
            'required': 'کلمه عبور را وارد کنید',
            'max_length': 'کلمه عبور باید حداکثر 20 کاراکتر باشد',
            'min_length': 'کلمه عبور باید حداقل 4 کاراکتر باشد'
        }
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(),
        min_length=4,
        max_length=20,
        error_messages={
            'required': 'تکرار کلمه عبور را وارد کنید'
        }
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(),
        validators=[validators.EmailValidator],
        error_messages={
            'required': 'ایمیل خود را وارد کنید'
        }
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'کلمه عبور را وارد کنید'
        }
    )


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(),
        label='ایمیل',
        max_length=100,
        validators=[validators.EmailValidator],
        error_messages={
            'required': 'ایمیل خود را وارد کنید',
            'max_length': 'ایمیل باید حداکثر 100 کاراکتر باشد'
        }
    )


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(),
        min_length=4,
        max_length=20,
        error_messages={
            'required': 'کلمه عبور را وارد کنید',
            'max_length': 'کلمه عبور باید حداکثر 20 کاراکتر باشد',
            'min_length': 'کلمه عبور باید حداقل 4 کاراکتر باشد'
        }
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(),
        min_length=4,
        max_length=20,
        error_messages={
            'required': 'تکرار کلمه عبور را وارد کنید'
        }
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'address', 'about_user']
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'avatar': 'تصویر پروفایل',
            'address': 'آدرس',
            'about_user': 'درباره شخص'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'avatar': forms.FileInput(),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5
            }),
            'about_user': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10
            })
        }


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label='کلمه عبور فعلی',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )
    new_password = forms.CharField(
        label='کلمه عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        validators=[
            validators.MinLengthValidator(4),
            validators.MaxLengthValidator(20)
        ],
        error_messages={
            'required': 'کلمه عبور جدید را وارد کنید',
            'max_length': 'کلمه عبور باید حداکثر 20 کاراکتر باشد',
            'min_length': 'کلمه عبور باید حداقل 4 کاراکتر باشد'
        }
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        validators=[
            validators.MinLengthValidator(4),
            validators.MaxLengthValidator(20)
        ],
        error_messages={
            'required': 'تکرار کلمه عبور را وارد کنید',
            'max_length': 'کلمه عبور باید حداکثر 20 کاراکتر باشد',
            'min_length': 'کلمه عبور باید حداقل 4 کاراکتر باشد'
        }
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('کلمه عبور و تکرار آن مغایرت دارند')

