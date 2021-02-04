from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from accounts.choices import TUITION_DEPARTMENTS
from accounts.forms import CourseForm
from accounts.forms import HODForm
from accounts.forms import LoginForm
from accounts.forms import StudentRegistrationForm
from accounts.forms import SubjectForm
from accounts.forms import TeacherForm
from accounts.forms import TraineeRegistrationForm
from accounts.forms import TrainerForm
from accounts.models import Course
from accounts.models import SelectedClass
from accounts.models import Subject
from accounts.models import User
from institute.forms import FeeForm
from institute.forms import SalaryForm
from project.email import send_email

tuition_departments = TUITION_DEPARTMENTS


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
    return redirect('home')


@login_required()
def change_password(request):
    title = 'Change Password'
    form = PasswordChangeForm(request.POST or None, request=request)
    if form.is_valid():
        form.save_password()
        return redirect('home')
    context = {'form': form, 'title': title}
    return render(request, 'change-password.html', context)


@login_required()
def hod_creation_view(request):
    if request.method == 'POST':
        form = HODForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save_user()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            send_email(
                subject="Your account created",
                message=f"Hi {user} \b Your HOD account for Vaadhyar is created please login using credentials given below\n\n Username: {email}\n Password: {password}",
                recipient_list=[user.email, ]
            )
            messages.success(request, 'Account created successfully')
            return redirect('hod-list')
    else:
        form = HODForm()
    context = {
        'title': 'Register HOD',
        'form': form
    }
    return render(request, 'accounts/forms/hod-form.html', context)


@login_required()
def teacher_creation_view(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save_user()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            send_email(
                subject="Your account created",
                message=f"Hi {user} \b Your Teacher account for Vaadhyar is created please login using credentials given below\n\n Username: {email}\n Password: {password}",
                recipient_list=[user.email, ]
            )
            messages.success(request, 'Account created successfully')
            return redirect('teachers-list')
    else:
        form = TeacherForm()
    context = {
        'title': 'Register Teacher',
        'form': form
    }
    return render(request, 'accounts/forms/teacher-form.html', context)


@login_required()
def trainer_creation_view(request):
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save_user()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            send_email(
                subject="Your account created",
                message=f"Hi {user} \b Your Trainer account for Vaadhyar is created please login using credentials given below\n\n Username: {email}\n Password: {password}",
                recipient_list=[user.email, ]
            )
            messages.success(request, 'Account created successfully')
            return redirect('trainers-list')
    else:
        form = TrainerForm()
    context = {
        'title': 'Register Trainer',
        'form': form
    }
    return render(request, 'accounts/forms/trainers-form.html', context)


def student_register_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            form.save_user()
            messages.success(request, 'Account created successfully')
            return redirect('home')
    else:
        form = StudentRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/student-registration.html', context)


def available_class_view(request):
    subjects = Subject.objects.filter(department=request.user.department)
    teachers = User.objects.filter(user_type='teacher')
    teacher_id_list = []
    for teacher in teachers:
        if teacher.get_subject in subjects:
            teacher_id_list.append(teacher.id)

    context = {
        'title': f'available classes for {request.user}',
        'list_items': teachers.filter(id__in=teacher_id_list)
    }
    return render(request, 'accounts/available-class.html', context)


def select_class_view(request, teacher_id):
    try:
        teacher = User.objects.get(id=teacher_id)
    except User.DoesNotExist:
        return HttpResponseNotFound()
    else:
        user = request.user
        if user.user_type == 'student':
            selected = SelectedClass.objects.create(student=user, subject=teacher.get_profile().subject,
                                                    teacher=teacher)
            selected.save()
            messages.success(request, "Class selected")
        messages.success(request, "Something went wrong")
    return redirect('dashboard')


def trainee_register_view(request):
    if request.method == 'POST':
        form = TraineeRegistrationForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            form.save_user()
            messages.success(request, 'Account created successfully')
            return redirect('home')
    else:
        form = TraineeRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/trainee-registration.html', context)


@login_required()
def hod_list_view(request):
    title = 'HOD'
    hod_list = User.objects.filter(user_type='hod')
    url = reverse('hod-create')
    context = {'title': title, 'list_items': hod_list, 'btn_text': "Add HOD", 'add_url': url}
    return render(request, 'accounts/user-list.html', context)


@login_required()
def teachers_list_view(request):
    title = 'Teachers'
    if request.user.user_type == 'student':
        profile = request.user.get_profile()
        selected_classes = profile.get_subjects_selected()
        teacher_list = [obj.teacher.id for obj in selected_classes]
        teacher_list = User.objects.filter(id__in=teacher_list)
    elif request.user.user_type == 'hod':
        if request.user.department == 'tuition':
            teacher_list = User.objects.filter(user_type='teacher', department__in=tuition_departments)
        else:
            teacher_list = User.objects.filter(user_type='teacher', department=request.user.department)
    else:
        teacher_list = User.objects.filter(user_type='teacher')
    url = reverse('teachers-create')
    context = {'title': title, 'list_items': teacher_list, 'btn_text': "Add Teacher", 'add_url': url}
    return render(request, 'accounts/user-list.html', context)


@login_required()
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


@login_required()
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


@login_required()
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
    url = reverse('trainers-create')
    context = {'title': title, 'list_items': user_list, 'btn_text': "Add Trainers", 'add_url': url}
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


@login_required
def subject_add(request):
    form = SubjectForm()
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject-create-list')
        else:
            print("not valid form")

    else:
        print("else")
        form = SubjectForm()
    return render(request, 'subjects/form-subject.html', {"form": form})


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


def delete_course(request, id):
    obj = Course.objects.get(id=id)
    obj.delete()
    return redirect('courses-list')


def edit_subject(request, id):
    obj = Subject.objects.get(id=id)
    form = SubjectForm(request.POST, obj)
    if request.method == 'POST':

        if form.is_valid():
            obj.department = form.cleaned_data.get('department')
            obj.name = form.cleaned_data.get('name')
            obj.save()
            return redirect('subject-create-list')
    form = SubjectForm()

    return render(request, 'subjects/edit-subject.html', {"form": form, "obj": obj})


def delete_subject(request, id):
    obj = Subject.objects.get(id=id)
    obj.delete()
    return redirect('subject-create-list')


@login_required()
def subject_create_list_view(request, ):
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


def user_profile_view(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponseNotFound()
    else:
        context = {
            'user_obj': user,
            'salary_form': SalaryForm(),
            'fee_form': FeeForm()
        }
        return render(request, 'accounts/user-profile.html', context)