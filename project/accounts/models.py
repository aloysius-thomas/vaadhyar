from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.choices import AVAILABLE_TIME_CHOICES
from accounts.choices import DEPARTMENT_CHOICES
from accounts.choices import GENDER_CHOICE
from accounts.choices import USER_TYPE
from accounts.validations import phone_regex


class User(AbstractUser):
    user_type = models.CharField(choices=USER_TYPE, max_length=16, default='admin')
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='profile-pic/')
    mobile_number = models.CharField(validators=[phone_regex], max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    place = models.CharField(max_length=62, blank=True, null=True)
    pin_code = models.IntegerField(blank=True, null=True)
    department = models.CharField(max_length=64, choices=DEPARTMENT_CHOICES)
    gender = models.CharField(max_length=6, blank=True, null=True, choices=GENDER_CHOICE)

    def __str__(self):
        return self.get_full_name() if self.get_full_name() else self.username

    def get_profile(self):
        if self.user_type == 'hod':
            return HOD.objects.get(user=self)
        elif self.user_type == 'teacher':
            return Teacher.objects.get(user=self)
        elif self.user_type == 'student':
            return Student.objects.get(user=self)
        elif self.user_type == 'trainer':
            return Trainers.objects.get(user=self)
        elif self.user_type == 'trainee':
            return Trainee.objects.get(user=self)
        else:
            return None

    @property
    def is_class_selected(self):
        if SelectedClass.objects.filter(user=self).count() == 0:
            return False
        else:
            return True

    @property
    def get_subject(self):
        if self.user_type != 'teacher':
            return None
        profile = self.get_profile()
        return profile.subject


class Course(models.Model):
    name = models.CharField(max_length=128)
    department = models.CharField(choices=DEPARTMENT_CHOICES[1:], max_length=64)

    def __str__(self):
        return self.name


class Subject(models.Model):
    department = models.CharField(choices=DEPARTMENT_CHOICES[1:], max_length=36)
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
    available_time = models.CharField(max_length=32, choices=AVAILABLE_TIME_CHOICES)
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE)
    salary = models.IntegerField()
    student_limit = models.IntegerField(default=5)

    def __str__(self):
        return f'{self.user} profile'

    @property
    def my_students(self):
        my_class = SelectedClass.objects.filter(teacher=self.user)
        student_id = [student.student.id for student in my_class]
        return User.objects.filter(id__in=student_id)


class Student(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=128)
    mother_name = models.CharField(max_length=128)
    guardian_number = models.CharField(validators=[phone_regex], max_length=20, blank=True, null=True)
    standard = models.CharField(max_length=20, blank=True, null=True)
    board = models.CharField(max_length=20, blank=True, null=True)
    school_name = models.CharField(max_length=256)
    fee = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.user} profile'

    def get_subjects_selected(self):
        subjects = SelectedClass.objects.filter(student=self.user)
        return subjects


class SelectedClass(models.Model):
    student = models.ForeignKey(to=User, on_delete=models.CASCADE)
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, blank=True, null=True)
    teacher = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='class_teacher')


class Trainers(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=128)
    experience = models.CharField(max_length=128)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    salary = models.IntegerField()
    available_time = models.CharField(max_length=32, choices=AVAILABLE_TIME_CHOICES)
    student_limit = models.IntegerField(default=5)

    def __str__(self):
        return f'{self.user} profile'


class Trainee(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=128)
    mother_name = models.CharField(max_length=128)
    guardian_number = models.CharField(validators=[phone_regex], max_length=20, blank=True, null=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=256)
    fee = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.user} profile'
