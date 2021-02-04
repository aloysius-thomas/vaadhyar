from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

from accounts.views import about_us
from accounts.views import change_password
from accounts.views import home_view
from accounts.views import dashboard_view
from accounts.views import login_view
from accounts.views import logout_view
from accounts.views import online_courses

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('about-us/', about_us, name='about-us'),
    path('online-courses/', online_courses, name='online-courses'),


    path('change-password/', change_password, name='change-password'),
    path('accounts/', include('accounts.urls')),
    path('institute/', include('institute.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
