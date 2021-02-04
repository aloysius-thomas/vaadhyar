from django.urls import path

from institute.views import add_fee_view
from institute.views import add_salary_view
from institute.views import attendance_list_view
from institute.views import class_details_view
from institute.views import complaint_create_list_view
from institute.views import complaint_list_view
from institute.views import complaint_response
from institute.views import exam_create_list_view
from institute.views import feedback_view
from institute.views import interview_create_list_view
from institute.views import leave_approve_view
from institute.views import leave_create_list_view
from institute.views import leave_recommend_view
from institute.views import leave_reject_view
from institute.views import leave_request_list_view
from institute.views import mark_as_absent_view
from institute.views import mark_as_present_view
from institute.views import mark_list
from institute.views import salary_history
from institute.views import students_attendance_sheet
from institute.views import study_material_list_add_view
from institute.views import teachers_attendance_sheet
from institute.views import time_table_view
from institute.views import update_mark

urlpatterns = [
    path('interviews/', interview_create_list_view, name='interviews'),
    path('study-material/<str:material_type>/', study_material_list_add_view, name='study-materials'),
    path('leave-request/', leave_create_list_view, name='leave-request-create-list'),
    path('leave-request/list/<str:user_type>/', leave_request_list_view, name='leave-request-list'),
    path('leave-request/<int:leave_id>/recommend/', leave_recommend_view, name='leave-recommend-view'),
    path('leave-request/<int:leave_id>/reject/', leave_reject_view, name='leave-reject-view'),
    path('leave-request/<int:leave_id>/approve/', leave_approve_view, name='leave-approve-view'),
    path('complaints/', complaint_create_list_view, name='complaint-create-list'),
    path('complaints/<str:user_type>/', complaint_list_view, name='complaint-list'),
    path('complaint/<int:c_id>/response/', complaint_response, name='complaint-response'),
    path('exams/', exam_create_list_view, name='exam-create-list'),
    path('exams/<int:exam_id>/mark-list/', mark_list, name='exam-mark-list'),
    path('exams/<int:result_id>/update/', update_mark, name='update-mark-list'),
    path('time-table/', time_table_view, name='time-table'),
    path('feedback/', feedback_view, name='feedback'),
    path('attendance/list/<str:user_type>/', attendance_list_view, name='attendance-list-view'),
    path('students-attendance-sheet/', students_attendance_sheet, name='students-attendance-sheet'),
    path('teachers-attendance-sheet/', teachers_attendance_sheet, name='teachers-attendance-sheet'),
    path('attendance/<int:attendance_id>mark-as-present/', mark_as_present_view, name='mark-as-present-view'),
    path('attendance/<int:attendance_id>mark-as-absent/', mark_as_absent_view, name='mark-as-absent-view'),
    path('<int:user_id>/add-salary/', add_salary_view, name='add-salary-view'),
    path('salary-history/', salary_history, name='salary-history'),
    path('<int:user_id>/add-fee/', add_fee_view, name='add-fee-view'),
    path('class-details>/', class_details_view, name='class-details'),

]
