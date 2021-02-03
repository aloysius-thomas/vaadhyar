from django.urls import path

from accounts.views import hod_creation_view
from accounts.views import hod_list_view
from accounts.views import students_list_view
from accounts.views import subject_create_list_view
from accounts.views import teacher_creation_view
from accounts.views import teachers_list_view
from accounts.views import trainees_list_view
from accounts.views import trainers_list_view
from accounts.views import courses
from accounts.views import course_add
from accounts.views import edit_course

urlpatterns = [
    path('hod/list/', hod_list_view, name='hod-list'),
    path('hod/create/', hod_creation_view, name='hod-create'),
    path('teachers/list/', teachers_list_view, name='teachers-list'),
    path('teachers/create/', teacher_creation_view, name='teachers-create'),
    path('students/list/', students_list_view, name='students-list'),
    path('trainees/list/', trainees_list_view, name='trainees-list'),
    path('trainers/list/', trainers_list_view, name='trainers-list'),
    path('courses/list/', courses, name='courses-list'),
    path('courses/add/', course_add, name='course-add'),
    path('edit_course/<int:id>/', edit_course, name='edit_course'),
    path('subjects/', subject_create_list_view, name='subject-create-list'),
]
