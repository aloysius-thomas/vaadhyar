from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=120, widget=forms.PasswordInput())


class CourseForm(forms.Form):
    course = forms.CharField(max_length=120)
