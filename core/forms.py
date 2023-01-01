from django import forms


class ContactUsForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name', 'required': "required"}))
    subject = forms.CharField(widget=forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Your subject', 'required': "required"}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your message', 'required': "required"}))
