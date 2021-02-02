from django.contrib import admin

# Register your models here.
from accounts.models import Course

admin.site.register(Course)