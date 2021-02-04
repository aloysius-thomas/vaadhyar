from django.contrib import admin

# Register your models here.
from .models import Course
from .models import Teacher
from .models import Trainee
from .models import User
from .models import SelectedClass

admin.site.register(Course)
admin.site.register(User)
admin.site.register(SelectedClass)
admin.site.register(Teacher)
admin.site.register(Trainee)
