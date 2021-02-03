from django import forms

from institute.models import Complaint
from institute.models import Interview
from institute.models import Leave
from institute.models import StudyMaterial


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = '__all__'


class StudyMaterialForm(forms.ModelForm):
    class Meta:
        model = StudyMaterial
        fields = {
            'name',
            'course',
            'subject',
            'file',
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
