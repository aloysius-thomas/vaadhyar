from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

from accounts.views import about_us
from accounts.views import change_password
from accounts.views import dashboard_view
from accounts.views import home_view
from accounts.views import login_view
from accounts.views import logout_view
from accounts.views import online_courses
from institute.views import ansys
from institute.views import autocad
from institute.views import autocadec
from institute.views import autocadmech
from institute.views import catia
from institute.views import civil
from institute.views import courseslist
from institute.views import cs
from institute.views import ds
from institute.views import ec
from institute.views import ecprim
from institute.views import ecrevit
from institute.views import etab
from institute.views import googles
from institute.views import java
from institute.views import mech
from institute.views import navis
from institute.views import nxcad
from institute.views import nxcam
from institute.views import nxnas
from institute.views import prim
from institute.views import prime
from institute.views import python
from institute.views import revit
from institute.views import revitmep
from institute.views import revitst
from institute.views import solid
from institute.views import stadd
from institute.views import tu
from institute.views import viewteacher
from institute.views import vray
from institute.views import web

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
    path('viewteacher/', viewteacher, name='viewteacher'),
    path('courseslist/', courseslist, name='courseslist'),
    path('civil/', civil, name='civil'),
    path('cs/', cs, name='cs'),
    path('mech/', mech, name='mech'),
    path('ec/', ec, name='ec'),
    path('autocad/', autocad, name='autocad'),
    path('ds/', ds, name='ds'),
    path('revit/', revit, name='revit'),
    path('googles/', googles, name='googles'),
    path('stadd/', stadd, name='stadd'),
    path('etab/', etab, name='etab'),
    path('vray/', vray, name='vray'),
    path('revitst/', revitst, name='revitst'),
    path('navis/', navis, name='navis'),
    path('prim/', prim, name='prim'),
    path('autocadmech/', autocadmech, name='autocadmech'),
    path('solid/', solid, name='solid'),
    path('catia/', catia, name='catia'),
    path('ansys/', ansys, name='ansys'),
    path('nxcad/', nxcad, name='nxcad'),
    path('nxcam/', nxcam, name='nxcam'),
    path('nxnas/', nxnas, name='nxnas'),
    path('revitmep/', revitmep, name='revitmep'),
    path('prime/', prime, name='prime'),
    path('autocadec/', autocadec, name='autocadec'),
    path('ecrevit/', ecrevit, name='ecrevit'),
    path('ecprim/', ecprim, name='ecprim'),
    path('java/', java, name='java'),
    path('web/', web, name='web'),
    path('python/', python, name='python'),
    path('tu/', tu, name='tu'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
