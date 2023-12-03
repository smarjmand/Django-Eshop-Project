from django.shortcuts import render, redirect
from django.views.generic import ListView
from .forms import ContactUsForm, ContactUsModelForm, ProfileForm
from .models import ContactUs, UserProfile
from django.views.generic.base import View
from django.views.generic.edit import FormView, CreateView
from site_module.models import SiteSettings


#------------------------------------------------------------------------
## contact us by using Form (function-based view):

'''def contact_page(request):
    form = ContactUsForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            contact = ContactUs(
                name=form.cleaned_data.get('name'),
                email=form.cleaned_data.get('email'),
                subject=form.cleaned_data.get('subject'),
                message=form.cleaned_data.get('message')
            )
            contact.save()
            return redirect('index_page')
    return render(request, 'contact_us.html', {'form': form})'''


#------------------------------------------------------------------------
## contact us by using ModelForm (function-based view):

'''def contact_page(request):
    form = ContactUsModelForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('index_page')
    return render(request, 'contact_us.html', {'form': form})'''


#------------------------------------------------------------------------
## contact us by using View (class-based view):

# class ContactPageView(View):
#     def get(self, request):
#         form = ContactUsModelForm()
#         return render(request, 'contact_us.html', {'form': form})
#
#     def post(self, request):
#         form = ContactUsModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index_page')
#         return render(request, 'contact_us.html', {'form': form})


#------------------------------------------------------------------------
## contact us by using FormView (class-based view):
'''class ContactPageView(FormView):
    template_name = 'contact_us.html'
    form_class = ContactUsModelForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)'''


#------------------------------------------------------------------------
## contact us by using CreateView (class-based view):

# using model directly :
# class ContactPageView(CreateView):
#     template_name = 'contact_us.html'
#     model = ContactUs
#     fields = ['name', 'email', 'subject', 'message']
#     success_url = '/contact-us/'


# using ModelForm :
class ContactPageView(CreateView):
    template_name = 'contact_us.html'
    form_class = ContactUsModelForm
    success_url = '/contact-us/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        setting: SiteSettings = SiteSettings.objects.filter(is_main_settings=True).first()
        context['setting'] = setting
        return context


#------------------------------------------------------------------------
## create profile by using View (class-based view):

'''class CreateProfileView(View):
    def get(self, request):
        form = ProfileForm()
        return render(request, 'create_profile.html', {'form': form})

    def post(self, request):
        submitted_form = ProfileForm(request.POST, request.FILES)
        if submitted_form.is_valid():
            received_image = UserProfile(image=request.FILES['user_image'])
            received_image.save()
            return redirect('create_profile_page')
        return redirect('create_profile_page', {'form': submitted_form})'''


#------------------------------------------------------------------------
## create profile by using CreateView (class-based view):
class CreateProfileView(CreateView):
    template_name = 'create_profile.html'
    model = UserProfile
    fields = '__all__'
    success_url = '/contact-us/create-profile'


#------------------------------------------------------------------------
## create profile by using View (class-based view):
class ProfileListView(ListView):
    model = UserProfile
    template_name = 'profiles_list.html'
    context_object_name = 'profiles'
