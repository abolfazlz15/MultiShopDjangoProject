from random import randint

from django.contrib.auth import login, logout
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, View

from .forms import CheckOTPForm, LoginForm, RegisterForm
from .models import OTPCode, User


class UserLoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.get(phone=data['phone'])
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return super().form_valid(form)


class UserRegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        randcode = randint(1000, 9999)
        data = form.cleaned_data
        OTPCode.objects.create(phone=data['phone'], code=randcode)
        cache.set(key='register', value={'phone': data['phone'], 'email': data['email'], 'password': data['password'], 'full_name': data['full_name'], 'code': randcode}, timeout=300)
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

            if OTPCode.objects.filter(code=data['code'], phone=data_cache['phone']).exists():
                otp = OTPCode.objects.get(code=data['code'], phone=data_cache['phone'])

                user = User.objects.create_user(phone=data_cache['phone'], email=data_cache['email'], full_name=data_cache['full_name'], password=data_cache['password'])

                login(request, user)
                otp.delete()
                return redirect('accounts:login')
            else:
                form.er('code', 'invalid data2')
        else:
            form.add_error('code', 'invalid data')

        return render(request, 'accounts/check_otp.html', {'form': form})
    