from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from accounts.models import User
from accounts.otp_service import OTP
from order.models import Order
from product.models import FavoriteProduct
from user_panel import forms


class IndexPageView(LoginRequiredMixin ,generic.TemplateView):
    template_name = 'user_panel/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        # order status in main page
        all_order = Order.objects.filter(user=self.request.user).values_list('status', flat=True)
        context['all_order'] = all_order.count()
        context['delivered_order'] = all_order.filter(status='Delivered').count()
        context['in_Progrssing_order'] = all_order.filter(status='In Progrssing').count()
        context['returned_order'] = all_order.filter(status='Returned').count()
        return context
    

class UserProfileView(LoginRequiredMixin, generic.View):
    def get(self, request):
        change_name_form = forms.ChangeNameForm()
        change_phone_form = forms.ChangePhoneForm()
        change_email_form = forms.ChangeEmailForm()
        change_profile_image_form = forms.ChangeProfileImageForm()

        context = {
            'change_name_form': change_name_form,
            'change_phone_form': change_phone_form,
            'change_email_form': change_email_form,
            'change_profile_image_form': change_profile_image_form,
        }
        return render(request, 'user_panel/user_profile.html', context)

    def post(self, request):
        user = User.objects.get(id=request.user.id)

        change_name_form = forms.ChangeNameForm()
        change_phone_form = forms.ChangePhoneForm()
        change_email_form = forms.ChangeEmailForm()
        change_profile_image_form = forms.ChangeProfileImageForm()

        if 'change_name_form' in request.POST:
            change_name_form = forms.ChangeNameForm(request.POST)

            if change_name_form.is_valid():
                user.full_name = change_name_form.cleaned_data['full_name']
                user.save()
                return redirect('user_panel:user_profile')
        
        elif 'change_email_form' in request.POST:
            change_email_form = forms.ChangeEmailForm(request.POST)
            if change_email_form.is_valid():
                email = change_email_form.cleaned_data['email']
                otp_code = OTP()
                otp_code.generate_otp(request.user.email)
                cache.set(key='change_email', value={'new_email': email, 'current_email': request.user.email}, timeout=300)
                return redirect('user_panel:confirm_email')


        elif 'change_phone_form' in request.POST:
            change_phone_form = forms.ChangePhoneForm(request.POST)
            if change_phone_form.is_valid():
                phone = change_phone_form.cleaned_data['phone']
                otp_code = OTP()
                otp_code.generate_otp(request.user.phone)
                cache.set(key='change_phone', value={'new_phone': phone, 'current_phone': request.user.phone}, timeout=300)
                return redirect('user_panel:confirm_phone')
        
        
        elif 'change_profile_image_form' in request.POST:
            change_profile_image_form = forms.ChangeProfileImageForm(request.POST, request.FILES)
            if change_profile_image_form.is_valid():
                
                user.profile_image = change_profile_image_form.cleaned_data['profile_image']
                user.save()
                return redirect('user_panel:user_profile')
        
        context = {
            'change_name_form': change_name_form,
            'change_phone_form': change_phone_form,
            'change_email_form': change_email_form,
            'change_profile_image_form': change_profile_image_form,
        }
        return render(request, 'user_panel/user_profile.html', context)


class ConfirmNewPhoneView(LoginRequiredMixin, generic.View):
    def get(self, request):
        form = forms.ConfirmNewPhoneForm()
        return render(request, 'user_panel/confirm_new_phone.html', context={'form': form})
    
    def post(self, request):
        form = forms.ConfirmNewPhoneForm(request.POST)
        if form.is_valid():
            otp_obj = OTP()
            data = form.cleaned_data
            user_data =  cache.get(key='change_phone')
            if user_data is None:
                messages.add_message(self.request, messages.ERROR, 'your code is worng')
            else:
                try:
                    if otp_obj.verify_otp(otp=data['code'], data=user_data['current_phone']):
                        user = get_object_or_404(User, phone=user_data['current_phone'])
                        user.phone = user_data['new_phone']
                        user.save()                
                        return redirect('user_panel:user_profile')
                    else:
                                        messages.add_message(self.request, messages.ERROR, 'your code is worng')
                    return render(request, 'user_panel/confirm_new_phone.html', context={'form': form})
                except:
                    messages.add_message(self.request, messages.ERROR, 'your code is worng')
                    return render(request, 'user_panel/confirm_new_phone.html', context={'form': form})
                
        return render(request, 'user_panel/confirm_new_phone.html', context={'form': form})


class ConfirmNewEmailView(LoginRequiredMixin, generic.View):
    def get(self, request):
        form = forms.ConfirmNewEmailFor()
        return render(request, 'user_panel/confirm_new_email.html', context={'form': form})
    
    def post(self, request):
        form = forms.ConfirmNewEmailFor(request.POST)
        if form.is_valid():
            otp_obj = OTP()
            data = form.cleaned_data
            user_data =  cache.get(key='change_email')
            if user_data is None:
                messages.add_message(self.request, messages.ERROR, 'your code is worng')
            else:
                try:
                    if otp_obj.verify_otp(otp=data['code'], data=user_data['current_email']):
                        user = get_object_or_404(User, email=user_data['current_email'])
                        user.email = user_data['new_email']
                        user.save()                
                        return redirect('user_panel:user_profile')
                    else:
                                        messages.add_message(self.request, messages.ERROR, 'your code is worng')
                    return render(request, 'user_panel/confirm_new_email.html', context={'form': form})
                except:
                    messages.add_message(self.request, messages.ERROR, 'your code is worng')
                    return render(request, 'user_panel/confirm_new_email.html', context={'form': form})
                
        return render(request, 'user_panel/confirm_new_email.html', context={'form': form})


class OrderListView(LoginRequiredMixin, generic.ListView):
    template_name = 'user_panel/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset
    

class FavoriteProductList(generic.ListView):
    model = FavoriteProduct
    template_name = 'user_panel/favorite_product_list.html'
    context_object_name = 'products'
    paginate_by = 1

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.model.objects.filter(user=self.request.user)

        return queryset