from django import forms

from accounts.models import User
from institute.models import Complaint
from institute.models import Exam
from institute.models import Fee
from institute.models import Feedback
from institute.models import Interview
from institute.models import Leave
from institute.models import Salary
from institute.models import StudyMaterial


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = '__all__'


class StudyMaterialForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(queryset=User.objects.filter(user_type__in=['teacher', 'trainer']), required=False)

    class Meta:
        model = StudyMaterial
        fields = {
            'name',
            'course',
            'subject',
            'file',
            'teacher',
        }
        help_texts = {
            'course': "Select any one of course or subject"
        }


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = {
            'complaint_to',
            'complaint',
        }


class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = {
            'from_date',
            'to_date',
            'reason',
        }


class ExamForm(forms.ModelForm):
    time = forms.TimeField()

    class Meta:
        model = Exam
        fields = {
            'course',
            'subject',
            'date',
            'time',
            'max_time',
            'max_score',
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = {
            'feedback'
        }


class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = {
            'month',
            'amount',
            'status',
            'pending',
        }


class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = {
            'fee_type',
            'amount',
            'status',
            'due',
        }
