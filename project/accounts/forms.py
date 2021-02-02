from django import forms
from django.contrib.auth import authenticate

from accounts.models import User


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=120, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = {'email'}

    def clean(self, *args, **kwargs):
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("invalid credentials")
        username = user.username
        if not username or not password:
            raise forms.ValidationError("Please enter both fields")
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("invalid credentials")

        return super(LoginForm, self).clean()
