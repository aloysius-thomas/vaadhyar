from django.urls import path

from institute.views import complaint_create_list_view
from institute.views import interview_create_list_view
from institute.views import study_material_list_add_view

urlpatterns = [
    path('interviews/', interview_create_list_view, name='interviews'),
    path('study-material/<str:material_type>/', study_material_list_add_view, name='study-materials'),
    path('complaints/', complaint_create_list_view, name='complaint-create-list'),
]
