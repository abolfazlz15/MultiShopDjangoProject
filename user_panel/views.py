from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from order.models import Order
from user_panel import forms
from accounts.models import User



class IndexPageView(LoginRequiredMixin ,generic.TemplateView):
    template_name = 'user_panel/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        # order status in main page
        all_order = Order.objects.filter(user=self.request.user).values_list('status', flat=True)
        context['delivered_order'] = all_order.filter(status='Delivered').count()
        context['in_Progrssing_order'] = all_order.filter(status='In Progrssing').count()
        context['returned_order'] = all_order.filter(status='Returned').count()
        return context
    

class UserProfileView(LoginRequiredMixin, generic.View):
    def get(self, request):
        
        change_name_form = forms.ChangeNameForm()
        # change_phone_form = forms.ChangePhoneForm()
        # change_email_form = forms.ChangeEmailForm()
        # change_profile_image_form = forms.ChangeProfileImageForm()

        context = {
            'change_name_form': change_name_form,
            # 'change_phone_form': change_phone_form,
            # 'change_email_form': change_email_form,
            # 'change_profile_image_form': change_profile_image_form,
        }
        return render(request, 'user_panel/user_profile.html', context)

    def post(self, request):
        change_name_form = forms.ChangeNameForm(request.POST)

        if change_name_form.is_valid():
            print('testtttttttttttttttttttttt', change_name_form.cleaned_data)
            user = User.objects.get(id=request.user.id)
            user.full_name = change_name_form.cleaned_data['full_name']
            user.save()
            return redirect('user_panel:user_profile')
        return redirect('user_panel:user_profile')
