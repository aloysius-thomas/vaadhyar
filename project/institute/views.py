from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.shortcuts import render

from accounts.choices import TUITION_DEPARTMENTS
from institute.forms import ComplaintForm
from institute.forms import ExamForm
from institute.forms import FeedbackForm
from institute.forms import FeeForm
from institute.forms import InterviewForm
from institute.forms import LeaveForm
from institute.forms import SalaryForm
from institute.forms import StudyMaterialForm
from institute.models import Attendance
from institute.models import Complaint
from institute.models import Exam
from institute.models import Feedback
from institute.models import Interview
from institute.models import Leave
from institute.models import Result
from institute.models import StudyMaterial
from institute.models import TimeTable
from institute.utils import generate_attendance
from institute.utils import generate_time_table


def viewteacher(request):
    return render(request, "publicapp/viewteacher.html", {})


def courseslist(request):
    return render(request, "publicapp/courses.html", {})


def civil(request):
    return render(request, "publicapp/civil.html", {})


def cs(request):
    return render(request, "publicapp/cs.html", {})


def mech(request):
    return render(request, "publicapp/mech.html", {})


def ec(request):
    return render(request, "publicapp/ec.html", {})


def autocad(request):
    return render(request, "publicapp/autocad.html", {})


def solid(request):
    return render(request, "publicapp/solid.html", {})


def ansys(request):
    return render(request, "publicapp/ansys.html", {})


def catia(request):
    return render(request, "publicapp/catia.html", {})


def ds(request):
    return render(request, "publicapp/ds.html", {})


def revit(request):
    return render(request, "publicapp/revit.html", {})


def googles(request):
    return render(request, "publicapp/googles.html", {})


def stadd(request):
    return render(request, "publicapp/stadd.html", {})


def etab(request):
    return render(request, "publicapp/etab.html", {})


def vray(request):
    return render(request, "publicapp/vray.html", {})


def revitst(request):
    return render(request, "publicapp/revitst.html", {})


def navis(request):
    return render(request, "publicapp/navis.html", {})


def prim(request):
    return render(request, "publicapp/prim.html", {})


def autocadmech(request):
    return render(request, "publicapp/autocadmech.html", {})


def nxcad(request):
    return render(request, "publicapp/nxcad.html", {})


def nxcam(request):
    return render(request, "publicapp/nxcam.html", {})


def nxnas(request):
    return render(request, "publicapp/nxnas.html", {})


def revitmep(request):
    return render(request, "publicapp/revitmep.html", {})


def prime(request):
    return render(request, "publicapp/prime.html", {})


def autocadec(request):
    return render(request, "publicapp/autocadec.html", {})


def ecrevit(request):
    return render(request, "publicapp/ecrevit.html", {})


def ecprim(request):
    return render(request, "publicapp/ecprim.html", {})


def java(request):
    return render(request, "publicapp/java.html", {})


def web(request):
    return render(request, "publicapp/web.html", {})


def python(request):
    return render(request, "publicapp/python.html", {})


def tu(request):
    return render(request, "publicapp/tu.html", {})


@login_required
def interview_create_list_view(request):
    user = request.user
    if user.is_superuser:
        list_items = Interview.objects.all()
    elif user.user_type == 'trainer':
        profile = user.get_profile
        list_items = Interview.objects.filter(course=profile.course)
    elif user.user_type == 'trainee':
        profile = user.get_profile()
        selected_subject = profile.get_subjects_selected()
        course_id_list = [course.course_id for course in selected_subject]
        list_items = Interview.objects.filter(course__in=course_id_list)
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
            if request.user.user_type == 'teacher':
                material.subject = request.user.get_subject
            elif request.user.user_type == 'trainer':
                material.subject = request.user.get_course
            else:
                pass
            if material_type != 'video':
                material.teacher = request.user
            material.save()
            return redirect('study-materials', material_type)
    else:
        form = StudyMaterialForm()
    list_items = StudyMaterial.objects.filter(material_type=material_type)
    if user.user_type in ['teacher', 'trainer']:
        list_items = list_items.filter(teacher=user)
    elif user.user_type == 'student':
        profile = user.get_profile()
        subjects = [subject.id for subject in profile.get_subjects_selected()]
        list_items = list_items.filter(subject_id__in=subjects)
    elif user.user_type == 'trainee':
        profile = user.get_profile()
        courses = [course.id for course in profile.get_subjects_selected()]
        list_items = list_items.filter(course_id__in=courses)
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
    if request.user.user_type == 'hod':
        list_items = list_items.filter(user__department=request.user.department, complaint_to='hod')
    elif request.user.is_superuser:
        list_items = list_items.filter(complaint_to='admin')
    else:
        list_items = []

    context = {
        'title': f"Complaints of {user_type.title()}",
        'list_items': list_items,
    }
    return render(request, 'institute/complaint-list.html', context)


@login_required()
def complaint_response(request, c_id):
    response = request.POST.get('response')
    print(response)
    print(request.POST)
    try:
        complaint = Complaint.objects.get(id=c_id)
    except Complaint.DoesNotExist:
        return HttpResponseNotFound()
    complaint.response = response
    complaint.save()
    messages.success(request, "Success")
    return redirect('complaint-list', complaint.user.user_type)


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
def leave_request_list_view(request, user_type):
    list_items = Leave.objects.filter(user__user_type=user_type)
    user = request.user
    if user.user_type == 'hod':
        if user.department == 'tuition':
            list_items = list_items.filter(user__department__in=TUITION_DEPARTMENTS)
        else:
            list_items = list_items.filter(user__department=user.department)

    elif user.user_type in ['teacher', 'trainer']:
        profile = user.get_profile()
        my_students = profile.my_students
        list_items = list_items.filter(user__in=my_students)
    elif user.is_superuser:
        list_items = list_items
    else:
        list_items = []

    context = {
        'title': f"{user_type.title()} Leave Request",
        'list_items': list_items,
    }
    return render(request, 'institute/leave-list.html', context)


@login_required()
def leave_recommend_view(request, leave_id):
    try:
        leave = Leave.objects.get(id=leave_id)
    except Leave.DoesNotExist:
        return HttpResponseNotFound()
    else:
        leave.status = 'recommended'
        leave.response = f"Your leave is recommended {request.user}, please wait for the approval of HOD"
        leave.save()
        return redirect('leave-request-list', leave.user.user_type)


@login_required()
def leave_reject_view(request, leave_id):
    try:
        leave = Leave.objects.get(id=leave_id)
    except Leave.DoesNotExist:
        return HttpResponseNotFound()
    else:
        leave.status = 'rejected'
        reason = request.POST.get('reason')
        leave.response = f"Your leave is rejected by {request.user} due to {reason}."
        leave.save()
        return redirect('leave-request-list', leave.user.user_type)


@login_required()
def leave_approve_view(request, leave_id):
    try:
        leave = Leave.objects.get(id=leave_id)
    except Leave.DoesNotExist:
        return HttpResponseNotFound()
    else:
        leave.status = 'approved'
        leave.response = f"Your leave is approved by {request.user}."
        leave.save()
        return redirect('leave-request-list', leave.user.user_type)


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


@login_required()
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


@login_required()
def attendance_list_view(request, user_type):
    generate_attendance()
    today = datetime.now().date()
    user = request.user
    date = request.GET.get('date', None)
    month_and_year = request.GET.get('month', None)
    if month_and_year:
        month = month_and_year[5:]
        month = int(month)
        year = month_and_year[:4]
        year = int(year)
    else:
        month = None
        year = None
    department = request.GET.get('department', None)
    attendance = Attendance.objects.filter(user__user_type=user_type, )
    if month or date or year or department:
        if month:
            attendance = attendance.filter(date__month=month)
        if date:
            attendance = attendance.filter(date__day=date)
        if year:
            attendance = attendance.filter(date__year=year)
        if department:
            attendance = attendance.filter(user__department=department)
    else:
        attendance = Attendance.objects.filter(date=today, user__user_type=user_type)
    if user.is_superuser:
        attendance = attendance
    elif user.user_type == 'hod':
        if user.department == 'tuition':
            attendance = attendance.filter(user__department__in=TUITION_DEPARTMENTS)
        else:
            attendance = attendance.filter(user__department=user.department)
    elif user.user_type == 'teacher':
        my_students = user.get_profile().my_students
        attendance = attendance.filter(user__in=my_students, subject=user.get_subject)
    elif user.user_type == 'trainer':
        my_students = user.get_profile().my_students
        attendance = attendance.filter(user__in=my_students, subject=user.get_course)
    elif user.user_type in ['student', 'trainee']:
        attendance = attendance.filter(user=user)
    else:
        attendance = []

    context = {
        "title": f"Attendance of {today.strftime('%d %B %Y')}",
        "list_items": attendance,
        "user_type": user_type,
        "btn_text": 'Filter',
    }
    return render(request, 'accounts/attendance-list.html', context)


@login_required()
def students_attendance_sheet(request):
    generate_attendance()
    today = datetime.now().date()
    user = request.user
    if user.user_type not in ['teacher', 'trainer']:
        return HttpResponseNotFound('Access denied')
    my_students = user.get_profile().my_students
    attendance = Attendance.objects.filter(date=today)
    if user.user_type == 'teacher':
        attendance = attendance.filter(user__in=my_students, subject=user.get_subject)
    elif user.user_type == 'trainer':
        attendance = attendance.filter(user__in=my_students, subject=user.get_course)
    else:
        attendance = []
    context = {
        'title': f"Mark Attendance of {today.strftime('%d %B %Y')}",
        "list_items": attendance,
    }
    return render(request, 'accounts/students-attendance-sheet.html', context)


def teachers_attendance_sheet(request):
    generate_attendance()
    today = datetime.now().date()
    user = request.user
    if user.user_type != 'hod':
        return HttpResponseNotFound()
    attendance = Attendance.objects.filter(date=today, user__user_type__in=['teacher', 'trainer'])
    if user.department == 'tuition':
        attendance = attendance.filter(user__department__in=TUITION_DEPARTMENTS)
    else:
        attendance = attendance.filter(user__department=user.department)
    context = {
        'title': f"Mark Attendance of {today.strftime('%d %B %Y')}",
        "list_items": attendance,
    }
    return render(request, 'accounts/students-attendance-sheet.html', context)


@login_required()
def mark_as_present_view(request, attendance_id):
    try:
        attendance = Attendance.objects.get(id=attendance_id)
    except Attendance.DoesNotExist:
        return HttpResponseNotFound()
    else:
        attendance.status = 'present'
        attendance.save()
        if request.user.user_type == 'hod':
            return redirect('teachers-attendance-sheet')
        else:
            return redirect('students-attendance-sheet')


@login_required()
def mark_as_absent_view(request, attendance_id):
    try:
        attendance = Attendance.objects.get(id=attendance_id)
    except Attendance.DoesNotExist:
        return HttpResponseNotFound()
    else:
        attendance.status = 'absent'
        attendance.save()
        if request.user.user_type == 'hod':
            return redirect('teachers-attendance-sheet')
        else:
            return redirect('students-attendance-sheet')


@login_required()
def add_salary_view(request, user_id):
    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            salary = form.save(commit=False)
            salary.user_id = user_id
            salary.save()
            return redirect('user-profile-details', int(user_id))
    return HttpResponseNotFound()


@login_required()
def add_fee_view(request, user_id):
    if request.method == 'POST':
        form = FeeForm(request.POST)
        if form.is_valid():
            fee = form.save(commit=False)
            fee.user_id = user_id
            fee.save()
            return redirect('user-profile-details', int(user_id))
    return HttpResponseNotFound()


@login_required()
def salary_history(request):
    context = {
        'title': "My Salary History",
        'list_items': request.user.salary_history
    }
    return render(request, 'institute/salary-history.html', context)


@login_required()
def mark_list(request, exam_id):
    today = datetime.now()
    exam_finished = False
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        return HttpResponseNotFound()
    else:
        my_students = exam.conducted_by.get_profile().my_students
        for student in my_students:
            Result.objects.get_or_create(exam=exam, attended_by=student)
        if today.date() > exam.date:
            exam_finished = True
        context = {
            'exam': exam,
            'exam_finished': exam_finished,
            'students_attended': Result.objects.filter(exam=exam)
        }

        return render(request, 'institute/mark-list.html', context)


@login_required()
def update_mark(request, result_id):
    try:
        result = Result.objects.get(id=result_id)
    except Result.DoesNotExist:
        return HttpResponseNotFound()
    else:
        mark = request.POST.get('mark' or None)
        result.mark = mark
        result.save()
        return redirect('exam-mark-list', result.exam.id)


@login_required()
def class_details_view(request):
    today = datetime.now().date()
    generate_time_table()
    user = request.user
    if user.user_type in ['teacher', 'trainer']:
        time_table = TimeTable.objects.filter(teacher=user, date=today)
    else:
        selected_class = user.get_profile().get_subjects_selected()
        teacher_id_list = [c.teacher_id for c in selected_class]
        time_table = TimeTable.objects.filter(teacher_id__in=teacher_id_list, date=today)

    context = {
        'title': f'My Class of {today}',
        'list_items': time_table
    }
    return render(request, 'institute/time-table.html', context)
