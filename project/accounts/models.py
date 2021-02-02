from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.choices import USER_TYPE
from accounts.validations import phone_regex


class User(AbstractUser):
    user_type = models.CharField(choices=USER_TYPE, max_length=16, default='admin')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='profile-pic/')
    mobile_number = models.CharField(validators=[phone_regex], max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    place = models.CharField(max_length=62, blank=True, null=True)
    pin_code = models.IntegerField(blank=True, null=True)
    department = models.CharField(max_length=32)
    gender = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.get_full_name() if self.get_full_name() else self.username


class Course(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class HOD(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=128)
    experience = models.CharField(max_length=128)
    salary = models.IntegerField()

    def __str__(self):
        return f'{self.user} profile'


class Teacher(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=128)
    experience = models.CharField(max_length=128)
    available_time = models.CharField(max_length=32)
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE)
    salary = models.IntegerField()

    def __str__(self):
        return f'{self.user} profile'


class Student(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=128)
    mother_name = models.CharField(max_length=128)
    guardian_number = models.CharField(validators=[phone_regex], max_length=20, blank=True, null=True)
    standard = models.CharField(max_length=20, blank=True, null=True)
    board = models.CharField(max_length=20, blank=True, null=True)
    school_name = models.CharField(max_length=256)
    fee = models.IntegerField()

    def __str__(self):
        return f'{self.user} profile'


class Trainers(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=128)
    experience = models.CharField(max_length=128)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    salary = models.IntegerField()

    def __str__(self):
        return f'{self.user} profile'


class Trainee(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=128)
    mother_name = models.CharField(max_length=128)
    guardian_number = models.CharField(validators=[phone_regex], max_length=20, blank=True, null=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    board = models.CharField(max_length=20, blank=True, null=True)
    school_name = models.CharField(max_length=256)
    fee = models.IntegerField()

    def __str__(self):
        return f'{self.user} profile'
