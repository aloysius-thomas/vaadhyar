from datetime import datetime

from accounts.models import User
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
