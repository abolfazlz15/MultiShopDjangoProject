from django import forms
from django.contrib.auth import get_user_model


class ChangeNameForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

# class ChangePhoneForm(forms.ModelForm):
#     phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     class Meta:
#         model = get_user_model()
#         fields = ('phone',)
     

# class ChangeEmailForm(forms.ModelForm):
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
#     class Meta:
#         model = get_user_model()
#         fields = ('email',)


# class ChangeProfileImageForm(forms.ModelForm):
#     profile_image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'exampleInputFile', 'type': 'file'}))

#     class Meta:
#         model = get_user_model()
#         fields = ('profile_image',)
