from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from accounts.choices import TUITION_DEPARTMENTS
from institute.forms import ComplaintForm
from institute.forms import ExamForm
from institute.forms import FeedbackForm
from institute.forms import InterviewForm
from institute.forms import LeaveForm
from institute.forms import StudyMaterialForm
from institute.models import Complaint
from institute.models import Exam
from institute.models import Feedback
from institute.models import Interview
from institute.models import Leave
from institute.models import StudyMaterial
from institute.models import TimeTable
from institute.utils import generate_time_table


@login_required
def interview_create_list_view(request):
    user = request.user
    if user.is_superuser:
        list_items = Interview.objects.all()
    elif user.user_type in ['trainer', 'trainee']:
        profile = user.get_profile
        list_items = Interview.objects.filter(course=profile.course)
    else:
        list_items = []
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Success")
            return redirect('interviews')
    else:
        form = InterviewForm()
    context = {
        'form': form,
        'title': 'Interviews',
        'list_items': list_items,
        'btn_text': "Add Interview",
    }
    return render(request, 'institute/interview-create-list.html', context)


@login_required()
def study_material_list_add_view(request, material_type):
    title = material_type.replace('-', ' ')
    title = title.title()
    user = request.user
    if request.method == 'POST':
        form = StudyMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.material_type = material_type
            material.uploaded_by = request.user
            material.save()
            return redirect('study-materials', material_type)
    else:
        form = StudyMaterialForm()
    list_items = StudyMaterial.objects.filter(material_type=material_type)
    if user.user_type == 'teacher':
        profile = user.get_profile()
        list_items = list_items.filter(subject=profile.subject)
    elif user.user_type == 'trainer':
        profile = user.get_profile()
        list_items = list_items.filter(course=profile.course)
    elif user.user_type == 'student':
        profile = user.get_profile()
        subjects = [subject.id for subject in profile.get_subjects_selected()]
        list_items = list_items.filter(subject_id__in=subjects)
    elif user.user_type == 'trainee':
        profile = user.get_profile()
        list_items = list_items.filter(course=profile.course)
    else:
        list_items = list_items
    context = {
        'form': form,
        'title': title,
        'material_type': material_type,
        'list_items': list_items,
        'btn_text': f"Add {title}",
    }
    return render(request, 'institute/study-materials-create-list.html', context)


@login_required()
def complaint_create_list_view(request):
    user = request.user
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            return redirect('complaint-create-list')
    else:
        form = ComplaintForm()
    list_items = Complaint.objects.filter(user=user)
    context = {
        'form': form,
        'title': "Register a Complaint",
        'list_items': list_items,
        'btn_text': f"New",
    }
    return render(request, 'institute/complaint-create-list.html', context)


@login_required()
def complaint_list_view(request, user_type):
    list_items = Complaint.objects.filter(user__user_type=user_type)
    if request.user.user_type in ['hod', 'teacher', 'trainer']:
        list_items = list_items.filter(user__department=request.user.department)

    context = {
        'title': f"Complaints of {user_type.title()}",
        'list_items': list_items,
    }
    return render(request, 'institute/complaint-list.html', context)


@login_required()
def leave_create_list_view(request):
    user = request.user
    if request.method == 'POST':
        form = LeaveForm(request.POST, request.FILES)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.status = 'pending'
            leave.save()
            return redirect('leave-request-create-list')
    else:
        form = LeaveForm()
    list_items = Leave.objects.filter(user=user)
    context = {
        'form': form,
        'title': "Leave Request",
        'list_items': list_items,
        'btn_text': f"New",
    }
    return render(request, 'institute/leave-request-list.html', context)


@login_required()
def exam_create_list_view(request):
    user = request.user
    if request.method == 'POST':
        form = ExamForm(request.POST, request.FILES)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.conducted_by = request.user
            exam.save()
            return redirect('exam-create-list')
    else:
        form = ExamForm()
    if user.user_type in ['teacher', 'trainer']:
        list_items = Exam.objects.filter(conducted_by=user)
    elif user.user_type in ['student', 'trainee']:
        list_items = Exam.objects.filter(conducted_by__department=user.department)
    else:
        list_items = []
    context = {
        'form': form,
        'title': "Exams",
        'list_items': list_items,
        'btn_text': f"New",
    }
    return render(request, 'institute/exam-create-list.html', context)


@login_required()
def time_table_view(request):
    today = datetime.now().date()
    generate_time_table()
    user = request.user
    if user.department == 'tuition':
        time_table = TimeTable.objects.filter(teacher__department__in=TUITION_DEPARTMENTS, date=today)
    else:
        time_table = TimeTable.objects.filter(teacher__department=user.department, date=today)

    context = {
        'title': f'Time Table of {user.department} Department: {today.strftime("%d %B %Y")}',
        'list_items': time_table
    }
    return render(request, 'institute/time-table.html', context)


def feedback_view(request):
    user = request.user
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('feedback')
    else:
        form = FeedbackForm()
    if user.user_type in ['trainee', 'student']:
        list_items = Feedback.objects.filter(user=user)
    elif user.user_type in ['trainer', 'teacher']:
        students = user.get_profile().my_students
        print(students)
        print(',,,,,,,,,')
        list_items = Feedback.objects.filter(user__in=students)
    else:
        list_items = []

    context = {
        'form': form,
        'title': "Feedback",
        'list_items': list_items,
        'btn_text': f"Add Today's Feedback",
    }
    return render(request, 'institute/feedback.html', context)
