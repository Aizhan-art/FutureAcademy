from django.contrib import admin
from .models import Project, StudentActivity, Event, Task, Student, News


admin.site.register(Project)
admin.site.register(StudentActivity)
admin.site.register(Event)
admin.site.register(Task)
admin.site.register(News)
admin.site.register(Student)

