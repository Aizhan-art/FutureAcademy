from django.contrib import admin
from .models import (Project, Task, Event, StudentActivity,
                     News, StudentAchievement, Student, Dashboard,
                     LessonSchedule, Diary)


admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Event)
admin.site.register(StudentActivity)
admin.site.register(News)
admin.site.register(StudentAchievement)
admin.site.register(Student)
admin.site.register(Dashboard)
admin.site.register(LessonSchedule)
admin.site.register(Diary)
