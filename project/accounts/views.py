from django.contrib import auth
from django.shortcuts import redirect
from django.shortcuts import render

from accounts.forms import LoginForm
from accounts.models import User

tuition_departments = []


def home_view(request):
    return render(request, 'home.html', {})


def dashboard_view(request):
    return render(request, 'dashboard.html', {})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)
            auth.login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    pass


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
