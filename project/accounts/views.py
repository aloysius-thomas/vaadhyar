from django.shortcuts import render


def home_view(request):
    return render(request, 'home.html', {})


def dashboard_view(request):
    return render(request, 'dashboard.html', {})


def hod_list_view(request):
    title = 'HOD'

    return render(request, 'accounts/hod-list.html', {})


def teachers_list_view(request):
    title = 'Teachers'

    return render(request, 'accounts/teachers-list.html', {})


def students_list_view(request):
    title = 'Students'

    return render(request, 'accounts/students-list.html', {})


def trainees_list_view(request):
    title = 'Trainees'

    return render(request, 'accounts/trainees-list.html', {})


def trainers_list_view(request):
    title = 'Trainers'

    return render(request, 'accounts/trainers-list.html', {})
