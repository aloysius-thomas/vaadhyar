from django.conf import settings
from django.conf.urls import url
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
    url(r'^courseslist', courseslist, name='courseslist'),
    url(r'^civil', civil, name='civil'),
    url(r'^cs', cs, name='cs'),
    url(r'^mech', mech, name='mech'),
    url(r'^ec', ec, name='ec'),
    url(r'^autocad', autocad, name='autocad'),
    url(r'^ds', ds, name='ds'),
    url(r'^revit', revit, name='revit'),
    url(r'^googles', googles, name='googles'),
    url(r'^stadd', stadd, name='stadd'),
    url(r'^etab', etab, name='etab'),
    url(r'^vray', vray, name='vray'),
    url(r'^revitst', revitst, name='revitst'),
    url(r'^navis', navis, name='navis'),
    url(r'^prim', prim, name='prim'),
    url(r'^autocadmech', autocadmech, name='autocadmech'),
    url(r'^solid', solid, name='solid'),
    url(r'^catia', catia, name='catia'),
    url(r'^ansys', ansys, name='ansys'),
    url(r'^nxcad$', nxcad, name='nxcad'),
    url(r'^nxcam$', nxcam, name='nxcam'),
    url(r'^nxnas$', nxnas, name='nxnas'),
    url(r'^revitmep$', revitmep, name='revitmep'),
    url(r'^prime$', prime, name='prime'),
    url(r'^autocadec$', autocadec, name='autocadec'),
    url(r'^ecrevit$', ecrevit, name='ecrevit'),
    url(r'^ecprim$', ecprim, name='ecprim'),
    url(r'^java$', java, name='java'),
    url(r'^web$', web, name='web'),
    url(r'^python$', python, name='python'),
    url(r'^tu$', tu, name='tu'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
