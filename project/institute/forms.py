from django import forms

from institute.models import Interview


class InterviewForm(forms.ModelForm):

    class Meta:
        model = Interview
        fields = '__all__'
