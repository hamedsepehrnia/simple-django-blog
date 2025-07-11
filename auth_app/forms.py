from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from auth_app.models import UserProfile


class RegisterForm1(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}, ),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),

        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password and confirm and password != confirm:
            raise forms.ValidationError("passwords don't match")
        if User.objects.filter(username=cleaned_data.get('username')).exists():
            raise forms.ValidationError("Username already taken")
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            raise forms.ValidationError("Email already taken")


class RegisterForm2(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_image', 'occupation', 'website')
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),

        }
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("username or password incorrect")
            self.user = user
        return self.cleaned_data