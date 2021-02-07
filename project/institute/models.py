from django.db import models

from accounts.models import Course
from accounts.models import Subject
from accounts.models import User
from institute.choices import ATTENDANCE_STATUS
from institute.choices import FEES_CHOICES
from institute.choices import LEAVE_STATUS
from institute.choices import MONTH_CHOICES
from institute.choices import STUDY_MATERIAL_TYPE


class Leave(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    response = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=16, choices=LEAVE_STATUS)

    def __str__(self):
        return f'Leave request of {self.user}'


class Feedback(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    feedback = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback from {self.user}'

    class Meta:
        ordering = ['-id', ]


class Complaint(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    complaint_to = models.CharField(max_length=16,
                                    choices=(('hod', 'HOD'), ('admin', 'Admin')))
    complaint = models.TextField()
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'complaint from {self.user}'


class Fee(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    fee_type = models.CharField(max_length=35, choices=FEES_CHOICES)
    amount = models.IntegerField()
    status = models.CharField(max_length=50)
    due = models.CharField(max_length=50)


class Salary(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    month = models.CharField(max_length=35, choices=MONTH_CHOICES)
    amount = models.IntegerField()
    status = models.CharField(max_length=50)
    pending = models.IntegerField()


class StudyMaterial(models.Model):
    name = models.CharField(max_length=32)
    material_type = models.CharField(choices=STUDY_MATERIAL_TYPE, max_length=16)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, blank=True, null=True)
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField(upload_to='study-material')
    teacher = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    uploaded_on = models.DateTimeField(auto_now_add=True)


class Exam(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, blank=True, null=True)
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, blank=True, null=True)
    conducted_by = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField()
    # Time in minutes
    time = models.TimeField(blank=True, null=True)
    max_time = models.IntegerField()
    max_score = models.IntegerField()

    def __str__(self):
        return f'{self.course} Exam  {self.date.strftime("%d %B %Y")}' if self.course else f'{self.subject} Exam  {self.date.strftime("%d %B %Y")}'


class Result(models.Model):
    exam = models.ForeignKey(to=Exam, on_delete=models.CASCADE, blank=True, null=True)
    attended_by = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    mark = models.IntegerField(blank=True, null=True)

    @property
    def grade(self):
        if self.mark:
            avg = (self.mark / self.exam.max_score) * 100
            if 91 <= avg <= 100:
                return 'A+'
            elif 81 <= avg < 91:
                return 'A'
            elif 71 <= avg < 81:
                return 'B+'
            elif 61 <= avg < 71:
                return 'B'
            elif 51 <= avg < 61:
                return 'C+'
            elif 41 <= avg < 51:
                return 'C'
            elif 33 <= avg < 41:
                return 'D+'
            else:
                return 'Failed'
        return 'Mark Not Published'


class TimeTable(models.Model):
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, blank=True, null=True)
    teacher = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='teacher_field')
    time = models.CharField(max_length=16)
    date = models.DateField()


class Attendance(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField()
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, blank=True, null=True)
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=12, choices=ATTENDANCE_STATUS, default='pending')


class Interview(models.Model):
    company = models.CharField(max_length=128)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-id',)
