from django.contrib import admin
from .models import Project, LessonSchedule, Diary


admin.site.register(Project)
admin.site.register(LessonSchedule)
admin.site.register(Diary)
