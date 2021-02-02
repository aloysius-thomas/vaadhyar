from django.shortcuts import render

from accounts.models import User

tuition_departments = []


def home_view(request):
    return render(request, 'home.html', {})


def dashboard_view(request):
    return render(request, 'dashboard.html', {})


def hod_list_view(request):
    title = 'HOD'
    hod_list = User.objects.filter(user_type='hod')
    context = {'title': title, 'list_items': hod_list, 'btn_text': "Add HOD"}
    return render(request, 'accounts/hod-list.html', context)


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
    return render(request, 'accounts/teachers-list.html', context)


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
    return render(request, 'accounts/students-list.html', context)


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
    context = {'title': title, 'list_items': user_list, 'btn_text': "Add Trainee"}
    return render(request, 'accounts/trainees-list.html', context)


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
    context = {'title': title, 'list_items': user_list, }
    return render(request, 'accounts/trainers-list.html', context)
