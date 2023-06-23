from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.views import generic

from accounts.otp_service import OTP

from .forms import AddAddressForm, CheckOTPForm, LoginForm, RegisterForm
from .models import User


class UserLoginView(generic.View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/login.html', context={'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            user = authenticate(username=clean_data['username'], password=clean_data['password'])
            if  user is not None:
                login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('core:home')
        return render(request, 'accounts/login.html', context={'form': form})
        

class UserRegisterView(generic.FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        data = form.cleaned_data
        otp_service = OTP()
        otp_service.generate_otp(data['phone'])
        cache.set(key='register', value={'phone': data['phone'], 'email': data['email'], 'password': data['password'],
                                         'full_name': data['full_name']}, timeout=300)
        return redirect('accounts:check-otp')


class CheckOTPView(generic.View):
    form_class = CheckOTPForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/check_otp.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data_cache = cache.get(key='register')
            otp_obj = OTP()
            if data is None:
                messages.add_message(request, messages.WARNING, 'this code not exist or invalid')
            try:
                if otp_obj.verify_otp(otp=data['code'], data=data_cache['phone']):
                    user = User.objects.create_user(phone=data_cache['phone'], email=data_cache['email'], full_name=data_cache['full_name'], password=data_cache['password'])
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('core:home')
            except:
                messages.add_message(request, messages.WARNING, 'this code not exist or invalid')
                return render(request, 'accounts/check_otp.html', {'form': form})

        return render(request, 'accounts/check_otp.html', {'form': form})


class LogoutView(LoginRequiredMixin, generic.View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')


class AddAddressView(LoginRequiredMixin, generic.View):
    def get(self, request):
        form = AddAddressForm()
        return render(request, 'accounts/add_address_form.html', context={'form': form})

    def post(self, request):
        if len(request.user.addresses.all()) > 2:
            return redirect('order:cart-detail')

        form = AddAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
        return render(request, 'accounts/add_address_form.html', context={'form': form})

