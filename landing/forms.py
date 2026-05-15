from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import DurianQuery, LeafIdentification


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class DurianQueryForm(forms.ModelForm):
    class Meta:
        model = DurianQuery
        fields = ['query_text', 'variety']
        widgets = {
            'query_text': forms.Textarea(
                attrs={'rows': 3, 'placeholder': 'Ask about durian leaves or identification...'}),
        }


class LeafUploadForm(forms.ModelForm):
    class Meta:
        model = LeafIdentification
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*', 'class': 'file-input'}),
        }