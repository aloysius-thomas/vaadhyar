from django.urls import path

from accounts.views import available_class_view
from accounts.views import course_add
from accounts.views import subject_add
from accounts.views import courses
from accounts.views import edit_course
from accounts.views import edit_subject
from accounts.views import delete_subject
from accounts.views import delete_course
from accounts.views import hod_creation_view
from accounts.views import hod_list_view
from accounts.views import select_class_view
from accounts.views import student_register_view
from accounts.views import students_list_view
from accounts.views import subject_create_list_view
from accounts.views import teacher_creation_view
from accounts.views import teachers_list_view
from accounts.views import trainee_register_view
from accounts.views import trainees_list_view
from accounts.views import trainer_creation_view
from accounts.views import trainers_list_view
from accounts.views import user_profile_view
from institute.views import class_details_view

urlpatterns = [
    path('<int:user_id>/profile/', user_profile_view, name='user-profile-details'),
    path('student/register/', student_register_view, name='student-register'),
    path('trainee/register/', trainee_register_view, name='trainee-register'),
    path('hod/list/', hod_list_view, name='hod-list'),
    path('hod/create/', hod_creation_view, name='hod-create'),
    path('teachers/list/', teachers_list_view, name='teachers-list'),
    path('teachers/create/', teacher_creation_view, name='teachers-create'),
    path('students/list/', students_list_view, name='students-list'),
    path('trainees/list/', trainees_list_view, name='trainees-list'),
    path('trainers/list/', trainers_list_view, name='trainers-list'),
    path('trainers/create/', trainer_creation_view, name='trainers-create'),
    path('courses/list/', courses, name='courses-list'),
    path('courses/add/', course_add, name='course-add'),
    path('subjects/add/', subject_add, name='subject-add'),
    path('edit_course/<int:id>/', edit_course, name='edit_course'),
    path('delete_course/<int:id>/', delete_course, name='delete_course'),
    path('edit_subject/<int:id>/', edit_subject, name='edit_subject'),
    path('delete_subject/<int:id>/', delete_subject, name='delete_subject'),
    path('subjects/', subject_create_list_view, name='subject-create-list'),
    path('available-class/', available_class_view, name='available-class'),
    path('select_class_view/<int:teacher_id>/', select_class_view, name='select-class'),
]
