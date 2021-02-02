from django.urls import path

from institute.views import interview_create_list_view

urlpatterns = [
    path('interviews/', interview_create_list_view, name='interviews'),
]
