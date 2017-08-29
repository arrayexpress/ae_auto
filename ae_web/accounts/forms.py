from django import forms
from .models import User


class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=5, max_length=100)
    password = forms.CharField(min_length=6, max_length=150)
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    email = forms.EmailField()
    is_admin = forms.BooleanField(required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).count():
            raise forms.ValidationError("username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count():
            raise forms.ValidationError("email already exists")
        return email

    def create(self,):
        data = self.cleaned_data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        analyst = User(username=username, email=email)
        analyst.set_password(password)
        analyst.first_name = data.get('first_name')
        analyst.last_name = data.get('last_name')
        analyst.save()
