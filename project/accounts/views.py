from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from accounts.forms import LoginForm
from accounts.models import User
from accounts.forms import CourseForm
from accounts.models import User, Course
from django.contrib.auth.decorators import login_required

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
    pass


def hod_creation_view(request):
    pass


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
    context = {'title': title, 'list_items': hod_list, 'btn_text': "Add HOD"}
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
    return render(request,'courses/courses_list.html',{"courses":cours,"title":title})

@login_required
def course_add(request):
    form = CourseForm()
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('course')
            print("F",name)

            obj=Course(name=name)
            obj.save()
            return redirect('/accounts/courses/list/')
        else:
            print("not valid form")

    else:
        print("else")
        form = CourseForm()
    return render(request,'courses/add-course.html',{"form":form})

