from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from accounts.forms import ChangePasswordForm
from accounts.forms import CourseForm
from accounts.forms import HODForm
from accounts.forms import LoginForm
from accounts.forms import SubjectForm
from accounts.models import Course
from accounts.models import Subject
from accounts.models import User

tuition_departments = []


def home_view(request):
    return render(request, 'home.html', {})


@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html', {})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print('form valid')
            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)
            auth.login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('dashboard')


def change_password(request):
    title = 'Change Password'
    form = ChangePasswordForm(request.POST or None, request=request)
    if form.is_valid():
        form.save_password()
        return redirect('home')
    context = {'form': form, 'title': title}
    return render(request, 'change-password.html', context)


def hod_creation_view(request):
    if request.method == 'POST':
        form = HODForm(request.POST, request.FILES)
        if form.is_valid():
            form.save_user()
            messages.success(request, 'Account created successfully')
            return redirect('hod-list')
    else:
        form = HODForm()
    context = {
        'title': 'Register HOD',
        'form': form
    }
    return render(request, 'accounts/forms/hod-form.html', context)


def teacher_creation_view(request):
    pass


def trainer_creation_view(request):
    pass


def student_register_view(request):
    pass


def trainee_register_view(request):
    pass


def hod_list_view(request):
    title = 'HOD'
    hod_list = User.objects.filter(user_type='hod')
    url = reverse('hod-create')
    context = {'title': title, 'list_items': hod_list, 'btn_text': "Add HOD", 'add_url': url}
    return render(request, 'accounts/user-list.html', context)


def teachers_list_view(request):
    title = 'Teachers'
    if request.user.user_type == 'student':
        teacher_list = User.objects.filter(user_type='teacher', department=request.user.department)
    elif request.user.user_type == 'hod':
        if request.user.department == 'tuition':
            teacher_list = User.objects.filter(user_type='teacher', department__in=tuition_departments)
        else:
            teacher_list = User.objects.filter(user_type='teacher', department=request.user.department)
    else:
        teacher_list = User.objects.filter(user_type='teacher')
    context = {'title': title, 'list_items': teacher_list, 'btn_text': "Add Teacher"}
    return render(request, 'accounts/user-list.html', context)


def students_list_view(request):
    title = 'Students'
    if request.user.user_type == 'teacher':
        user_list = User.objects.filter(user_type='student', department=request.user.department)
    elif request.user.user_type == 'hod':
        if request.user.department == 'tuition':
            user_list = User.objects.filter(user_type='student', department__in=tuition_departments)
        else:
            user_list = User.objects.filter(user_type='student', department=request.user.department)
    else:
        user_list = User.objects.filter(user_type='student')
    context = {'title': title, 'list_items': user_list}
    return render(request, 'accounts/user-list.html', context)


def trainees_list_view(request):
    title = 'Trainees'
    if request.user.user_type == 'trainer':
        user_list = User.objects.filter(user_type='trainee', department=request.user.department)
    elif request.user.user_type == 'hod':
        if request.user.department == 'tuition':
            user_list = User.objects.filter(user_type='trainee', department__in=tuition_departments)
        else:
            user_list = User.objects.filter(user_type='trainee', department=request.user.department)
    else:
        user_list = User.objects.filter(user_type='trainee')
    context = {'title': title, 'list_items': user_list}
    return render(request, 'accounts/user-list.html', context)


def trainers_list_view(request):
    title = 'Trainers'
    if request.user.user_type == 'trainee':
        user_list = User.objects.filter(user_type='trainer', department=request.user.department)
    elif request.user.user_type == 'hod':
        if request.user.department == 'tuition':
            user_list = User.objects.filter(user_type='trainer', department__in=tuition_departments)
        else:
            user_list = User.objects.filter(user_type='trainer', department=request.user.department)
    else:
        user_list = User.objects.filter(user_type='trainer')
    context = {'title': title, 'list_items': user_list, 'btn_text': "Add Trainers"}
    return render(request, 'accounts/user-list.html', context)


def courses(request):
    title = 'Courses'
    if request.user.is_superuser:
        cours = Course.objects.all().order_by('-id')
    return render(request, 'courses/courses_list.html', {"courses": cours, "title": title})


@login_required
def course_add(request):
    form = CourseForm()
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('course')

            obj = Course(name=name)
            obj.save()
            return redirect('/accounts/courses/list/')
        else:
            print("not valid form")

    else:
        print("else")
        form = CourseForm()
    return render(request, 'courses/add-course.html', {"form": form})


def edit_course(request, id):
    obj = Course.objects.get(id=id)
    form = CourseForm(request.POST, obj)
    if request.method == 'POST':

        if form.is_valid():
            obj.name = form.cleaned_data.get('course')
            obj.save()
            return redirect('/accounts/courses/list/')
    form = CourseForm()

    return render(request, 'courses/edit-course.html', {"form": form, "obj": obj})


def subject_create_list_view(request, subject_id=0):
    if subject_id != 0:
        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            return HttpResponseNotFound()

        form = SubjectForm(request.POST, instance=subject)
    else:
        form = SubjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('subject-create-list')
    context = {
        'title': 'Subjects',
        'form': form,
        'btn_text': "Add Subject",
        'list_items': Subject.objects.all(),
    }
    return render(request, 'accounts/subject-list.html', context)
