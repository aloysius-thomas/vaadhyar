from django.contrib import admin

# Register your models here.
from .models import Course
from .models import Teacher
from .models import User

admin.site.register(Course)
admin.site.register(User)
admin.site.register(Teacher)
