from random import randint

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView, View

from .forms import CheckOTPForm, LoginForm, RegisterForm, AddAddressForm
from .models import OTPCode, User
from django.contrib.auth import authenticate


class UserLoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        data = form.cleaned_data
        user = authenticate(username=data['username'], password=data['password'])
        if  user is not None:
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        else:
            messages.add_message(self.request, messages.ERROR, 'your phone|email or password is worng')
        return super().form_valid(form)


class UserRegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        randcode = randint(1000, 9999)
        data = form.cleaned_data
        OTPCode.objects.create(phone=data['phone'], code=randcode)
        cache.set(key='register', value={'phone': data['phone'], 'email': data['email'], 'password': data['password'],
                                         'full_name': data['full_name'], 'code': randcode}, timeout=300)
        print(randcode)
        return redirect('accounts:check-otp')


class CheckOTPView(View):
    form_class = CheckOTPForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/check_otp.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data_cache = cache.get(key='register')

            try:
                otp = OTPCode.objects.get(code=data['code'], phone=data_cache['phone'])
                expiration_date = otp.expiration_date + timezone.timedelta(minutes=2)
                if expiration_date < timezone.now():
                    otp.delete()
                    messages.add_message(request, messages.WARNING, 'Your code verification time is over')
                    return render(request, 'accounts/check_otp.html', {'form': form})

                elif OTPCode.objects.filter(code=data['code'], phone=data_cache['phone']).exists():

                    user = User.objects.create_user(phone=data_cache['phone'], email=data_cache['email'],
                                                    full_name=data_cache['full_name'], password=data_cache['password'])

                    login(request, user)
                    otp.delete()
                    return redirect('accounts:login')

            except:
                messages.add_message(request, messages.ERROR, 'Your code is not valid')
                return render(request, 'accounts/check_otp.html', {'form': form})

        return render(request, 'accounts/check_otp.html', {'form': form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')


class AddAddressView(LoginRequiredMixin, View):
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

