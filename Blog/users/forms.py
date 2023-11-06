from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from.models import Profile
from django.contrib.auth import get_user_model

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "Username or password is invalid"
        ),
        'inactive': ("This account is inactive."),
    }

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(max_length=100, required=True)
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password1', 'password2', 'username','first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        User = get_user_model()
        # Check if the email is already in use
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        # Check if the password meets the minimum length requirement
        if len(password1) < 8:
            raise forms.ValidationError('This password is too short. It must contain at least 8 characters.')
        return password1

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        # Check if both email and password are provided
        if not email and not password1:
            raise forms.ValidationError('Email and password are required.')
        return cleaned_data

class UserUpdateForm(forms.ModelForm):
  
  class Meta:
    model = User
    fields = ['username','first_name','last_name']

  def clean_username(self):
        username = self.cleaned_data.get('username')
        # Check if the new username already exists in the database
        User = get_user_model()
        existing_user = User.objects.exclude(pk=self.instance.pk).filter(username=username).first()

        if existing_user:
            raise forms.ValidationError(f'User already exist with the username {existing_user}')
        
        return username

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['uid']