from datetime import datetime

from accounts.models import User
from institute.models import Attendance
from institute.models import TimeTable


def generate_time_table():
    today = datetime.now().date()

    teachers = User.objects.filter(user_type='teacher')
    trainers = User.objects.filter(user_type='trainer')
    for teacher in teachers:
        profile = teacher.get_profile()
        TimeTable.objects.get_or_create(teacher=teacher, subject=profile.subject, time=profile.available_time,
                                        date=today)

    for trainer in trainers:
        profile = trainer.get_profile()
        TimeTable.objects.get_or_create(teacher=trainer, course=profile.course, time=profile.available_time,
                                        date=today)


def generate_attendance():
    today = datetime.now().date()
    teachers = User.objects.filter(user_type__in=['teacher', 'trainer'])
    students = User.objects.filter(user_type__in=['student', 'trainee'])

    for teacher in teachers:
        Attendance.objects.get_or_create(user=teacher, date=today)

    for student in students:
        selected_class = student.selected_class
        for item in selected_class:
            if student.user_type == 'student':
                Attendance.objects.get_or_create(user=student, date=today, subject=item.subject)
            elif student.user_type == 'trainee':
                Attendance.objects.get_or_create(user=student, date=today, course=item.course)
            else:
                continue
