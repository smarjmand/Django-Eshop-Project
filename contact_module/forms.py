from django import forms
from .models import ContactUs


#------------------------------------------------------------------------
## Form for ContactUs model :
class ContactUsForm(forms.Form):
    name = forms.CharField(
        label='نام و نام خانوادگی',
        max_length=100,
        error_messages={
            'required': 'نام و نام خانوادگی خود را وارد کنید'
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام و نام خانوادگی'
        })
    )
    email = forms.EmailField(
        label='ایمیل',
        max_length=100,
        error_messages={
            'required': 'ایمیل خود را وارد کنید'
        },
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل'
        })
    )
    subject = forms.CharField(
        label='موضوع',
        max_length=100,
        error_messages={
            'required': 'موضوع پیام را مشخص کنید'
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'موضوع'
        })
    )
    message = forms.CharField(
        label='متن پیام',
        error_messages={
            'required': 'متن پیام را وارد کنید'
        },
        widget=forms.Textarea(attrs={
            'placeholder': 'متن پیام',
            'class': 'form-control',
            'rows': 5,
            'id': 'message'
        })
    )


#------------------------------------------------------------------------
## ModelForm for ContactUs model :
class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'id': 'message'
            })
        }
        error_messages = {
            'name': {
                'required': 'نام و نام خانوادگی خود را وارد کنید'
            },
            'email': {
                'required': 'وارد کردن ایمیل الزامی است'
            },
            'subject': {
                'required': 'موضوع را مشخص کنید'
            },
            'message': {
                'required': 'پیام را وارد کنید'
            },
        }


#------------------------------------------------------------------------
## Form for profile-image:
class ProfileForm(forms.Form):
    # user_image = forms.FileField()
    user_image = forms.ImageField()
