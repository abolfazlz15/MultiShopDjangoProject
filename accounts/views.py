from random import randint
from uuid import uuid4

from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, View

from .forms import CheackOTPForm, LoginForm, RegisterForm
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


class UserRegisterView(View):
    form_class = RegisterForm
    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            randcode = randint(1000, 9999)
            data = form.cleaned_data
            token = str(uuid4())
            OTPCode.objects.create(token=token, code=randcode, phone=data['phone'])
            print(randcode)
            return redirect(reverse('accounts:check-otp') + f'?token={token}')
    

class CheckOTPView(View):
    form_class = CheackOTPForm
    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/check_otp.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            token = request.GET.get('token')
            if OTPCode.objects.filter(code=data['code'], token=token).exists():
                otp = OTPCode.objects.get(token=token)
                user, is_created = User.objects.get_or_create(phone=otp.phone)
                login(request, user)
                otp.delete()
                return redirect('core:home')
        else:
            form.add_error('phone', 'invalid data')

        return render(request, 'accounts/check_otp.html', {'form': form})
    