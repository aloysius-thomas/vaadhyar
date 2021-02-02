from django.urls import path

from accounts.views import hod_list_view
from accounts.views import students_list_view
from accounts.views import teachers_list_view
from accounts.views import trainees_list_view
from accounts.views import trainers_list_view

urlpatterns = [
    path('hod/list/', hod_list_view, name='hod-list'),
    path('teachers/list/', teachers_list_view, name='teachers-list'),
    path('students/list/', students_list_view, name='students-list'),
    path('trainees/list/', trainees_list_view, name='trainees-list'),
    path('trainers/list/', trainers_list_view, name='trainers-list'),
]
