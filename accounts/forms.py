from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core import validators
from django.core.exceptions import ValidationError

from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone', 'email', 'username')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('phone', 'password', 'email', 'username', 'is_active', 'is_admin', 'is_superuser')


class LoginForm(forms.Form):
    phone = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your phone'}), validators=[validators.MaxLengthValidator(11)])
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'enter your password'})
    )

    def clean_password(self):
        user = authenticate(phone=self.cleaned_data.get('phone'), password=self.cleaned_data.get('password'))
        if user is not None:
            return self.cleaned_data.get('password')
        raise ValidationError('username or password is wrong', code='invalid_info')


class RegisterForm(forms.Form):
    phone = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your phone'}), validators=[validators.MaxLengthValidator(11)])
    # password1 = forms.CharField(widget=forms.PasswordInput(
    #     attrs={'class': 'form-control', 'placeholder': 'enter your password'}), validators=[validators.MinLengthValidator(8)])
    # password2 = forms.CharField(widget=forms.PasswordInput(
    #     attrs={'class': 'form-control', 'placeholder': 'enter your password'})
    # )

    # def clean_password1(self):
    #     password1 = self.cleaned_data.get('password1')
    #     try:
    #         password_validation.validate_password(password1)
    #     except forms.ValidationError as error:

    #         self.add_error('password1', error)
    #     return password1

    # def clean_password2(self):
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')

    #     if password1 != password2:
    #         raise ValidationError('رمز ورود با تکرار رمزورود برابر نیست', code='invalid_info')



class CheackOTPForm(forms.Form):
    code = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your code'}), validators=[validators.MaxLengthValidator(4)])


