from django import forms
from django.contrib.auth import authenticate

from accounts.choices import ADMIN_DEPARTMENT_CHOICES
from accounts.choices import AVAILABLE_TIME_CHOICES
from accounts.models import Course
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


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = {
            'username',
            'first_name',
            'last_name',
            'email',
            'image',
            'mobile_number',
            'date_of_birth',
            'address',
            'place',
            'pin_code',
            'department',
            'gender',
        }


def get_user_instance(data):
    username = data.get('username')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    password = data.get('password')
    address = data.get('address', None)
    image = data.get('image', None)
    date_of_birth = data.get('date_of_birth', None)
    place = data.get('place', None)
    pin_code = data.get('pin_code', None)
    department = data.get('department')
    gender = data.get('gender')
    mobile_number = data.get('mobile_number', None)
    email = data.get('email')

    user = User(username=username, first_name=first_name, last_name=last_name,
                address=address, mobile_number=mobile_number, email=email, image=image, date_of_birth=date_of_birth,
                place=place, pin_code=pin_code, department=department, gender=gender)
    user.set_password(password)
    user.save()
    return user


class HODForm(UserForm):
    department = forms.ChoiceField(choices=ADMIN_DEPARTMENT_CHOICES)
    qualification = forms.CharField(required=False)
    experience = forms.CharField(required=False)
    salary = forms.IntegerField()

    def save_user(self):
        from accounts.models import HOD
        user = get_user_instance(self.cleaned_data)
        user.user_type = 'hod'
        user.save()
        qualification = self.cleaned_data.get('qualification', None)
        experience = self.cleaned_data.get('experience', None)
        salary = self.cleaned_data.get('salary', None)
        profile = HOD(user=user, experience=experience, qualification=qualification,
                      salary=salary)
        profile.save()
        return user


class TeacherForm(UserForm):
    qualification = forms.CharField(required=False)
    experience = forms.CharField(required=False)
    available_time = forms.ChoiceField(choices=AVAILABLE_TIME_CHOICES)
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    salary = forms.IntegerField()

    def save_user(self):
        from accounts.models import Teacher
        user = get_user_instance(self.cleaned_data)
        user.user_type = 'teacher'
        user.save()
        qualification = self.cleaned_data.get('qualification', None)
        experience = self.cleaned_data.get('experience', None)
        salary = self.cleaned_data.get('salary', None)
        available_time = self.cleaned_data.get('available_time')
        subject = self.cleaned_data.get('subject')
        profile = Teacher(user=user, experience=experience, qualification=qualification,
                          salary=salary, available_time=available_time, subject=subject)
        profile.save()
        return user


class TrainerForm(UserForm):
    qualification = forms.CharField(required=False)
    experience = forms.CharField(required=False)
    available_time = forms.ChoiceField(choices=AVAILABLE_TIME_CHOICES)
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    salary = forms.IntegerField()

    def save_user(self):
        from accounts.models import Trainers
        user = get_user_instance(self.cleaned_data)
        user.user_type = 'trainer'
        user.save()
        qualification = self.cleaned_data.get('qualification', None)
        experience = self.cleaned_data.get('experience', None)
        salary = self.cleaned_data.get('salary', None)
        available_time = self.cleaned_data.get('available_time')
        course = self.cleaned_data.get('course')
        profile = Trainers(user=user, experience=experience, qualification=qualification,
                           salary=salary, available_time=available_time, course=course)
        profile.save()
        return user
