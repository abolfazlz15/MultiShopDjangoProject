from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator, MinLengthValidator
from accounts.models import User
from django.core.exceptions import ValidationError


class ChangeNameForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), validators=[MaxLengthValidator(120), MinLengthValidator(3)])


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)

        if user:
            raise ValidationError('This email already exists.', code='invalid_email')
        return email


class ChangePhoneForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        user = User.objects.filter(phone=phone)

        if user:
            raise ValidationError('this phone number already exist', code='invalid_phone')    
        return phone


class ChangeProfileImageForm(forms.ModelForm):
    profile_image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'exampleInputFile', 'type': 'file'}))

    class Meta:
        model = get_user_model()
        fields = ('profile_image',)

    def clean_profile_image(self):
        image = self.cleaned_data['profile_image']
        if image:
            if image.size > 4*1024*1024:
                raise ValidationError('Image file too large ( > 4mb )', code='invalid_phone') 
            return image
        else:
            raise ValidationError("Couldn't read uploaded image")



class ConfirmNewPhoneForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), validators=[MaxLengthValidator(4)])


class ConfirmNewEmailFor(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), validators=[MaxLengthValidator(4)])
