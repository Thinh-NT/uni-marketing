from django import forms
from django.forms import fields
from .models import Signup


class EmailSignupForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'type': 'email',
    }))

    class Meta:
        model = Signup
        fields = ('email', )
