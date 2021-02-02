from django.urls import path

from accounts.views import hod_list_view

urlpatterns = [
    path('hod/list/', hod_list_view, name='hod-list'),
]
