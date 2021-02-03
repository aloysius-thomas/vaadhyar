from django import forms
from django.contrib.auth import authenticate

from accounts.models import Subject
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


class CourseForm(forms.Form):
    course = forms.CharField(max_length=120)


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = "__all__"


class ChangePasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {}

    current_password = forms.PasswordInput()
    new_password = forms.PasswordInput()
    confirm_password = forms.PasswordInput()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        print(self.cleaned_data)
        print(';;;;;;;;;;;;;;;;;;')
        current_password = self.cleaned_data["current_password"]
        new_password = self.cleaned_data["new_password"]
        confirm_password = self.cleaned_data["confirm_password"]
        user = self.request.user
        user = authenticate(username=user.username, password=current_password)
        if not user:
            raise forms.ValidationError("invalid password")
        if new_password != confirm_password:
            raise forms.ValidationError("The password doesn't match")

        return super(ChangePasswordForm, self).clean()

    def save_password(self):
        user = self.request.user
        new_password = self.cleaned_data["new_password"]
        user.set_password(new_password)
        user.save()
