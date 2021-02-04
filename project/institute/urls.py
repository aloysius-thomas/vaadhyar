from django.urls import path

from institute.views import add_fee_view
from institute.views import add_salary_view
from institute.views import attendance_list_view
from institute.views import complaint_create_list_view
from institute.views import complaint_list_view
from institute.views import complaint_response
from institute.views import exam_create_list_view
from institute.views import feedback_view
from institute.views import interview_create_list_view
from institute.views import leave_create_list_view
from institute.views import study_material_list_add_view
from institute.views import time_table_view

urlpatterns = [
    path('interviews/', interview_create_list_view, name='interviews'),
    path('study-material/<str:material_type>/', study_material_list_add_view, name='study-materials'),
    path('leave-request/', leave_create_list_view, name='leave-request-create-list'),
    path('complaints/', complaint_create_list_view, name='complaint-create-list'),
    path('complaints/<str:user_type>/', complaint_list_view, name='complaint-list'),
    path('complaint/<int:c_id>/response/', complaint_response, name='complaint-response'),
    path('exams/', exam_create_list_view, name='exam-create-list'),
    path('time-table/', time_table_view, name='time-table'),
    path('feedback/', feedback_view, name='feedback'),
    path('attendance/list/<str:user_type>/', attendance_list_view, name='attendance-list-view'),
    path('<int:user_id>/add-salary/', add_salary_view, name='add-salary-view'),
    path('<int:user_id>/add-fee/', add_fee_view, name='add-fee-view'),
]
