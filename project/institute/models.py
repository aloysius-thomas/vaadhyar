from django.db import models

from accounts.models import Course
from accounts.models import Subject
from accounts.models import User
from institute.choices import FEES_CHOICES
from institute.choices import MONTH_CHOICES
from institute.choices import STATUS
from institute.choices import STUDY_MATERIAL_TYPE


class Leave(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    response = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=16, choices=STATUS)

    def __str__(self):
        return f'Leave request of {self.user}'


class Feedback(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    feedback = models.TextField()

    def __str__(self):
        return f'Feedback from {self.user}'


class Complaint(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    complaint_to = models.CharField(max_length=16,
                                    choices=(('hod', 'HOD'), ('teacher', 'Teacher'), ('trainer', 'Trainer')))
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
    uploaded_by = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    video_approved = models.BooleanField(default=False)


class Exam(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, blank=True, null=True)
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, blank=True, null=True)
    conducted_by = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    conducted_on = models.DateTimeField()
    # Time in minutes
    date = models.DateField()
    max_time = models.IntegerField()
    max_score = models.IntegerField()

    def __str__(self):
        return f'{self.course} Exam in {self.date}' if self.course else f'{self.subject} Exam in {self.date}'


class Result(models.Model):
    exam = models.ForeignKey(to=Exam, on_delete=models.CASCADE, blank=True, null=True)
    attended_by = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    mark = models.IntegerField()


class TimeTable(models.Model):
    student = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='student_field')
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, blank=True, null=True)
    teacher = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='teacher_field')
    time = models.CharField(max_length=16)
    date = models.DateField()


class Attendance(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=12, choices=STATUS)


class Interview(models.Model):
    company = models.CharField(max_length=128)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-id',)
