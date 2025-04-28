from user.models import MyUser

from django.db import models
from django.contrib.auth import get_user_model

MyUserUser = get_user_model()


class Project(models.Model):
    title = models.CharField(max_length=225, verbose_name='Название проекта')
    description = models.TextField(verbose_name='Описание проекта')
    main_cover = models.ImageField(upload_to='media/projects/main_cover', verbose_name='Главное фото')
    deadline = models.DateField(verbose_name='Дедлайн', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Task(models.Model):
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    main_cover = models.ImageField(upload_to='media/projects/main_cover', verbose_name='Главное фото')
    is_active = models.BooleanField(default=True)
    responsible_user = models.ForeignKey(MyUserUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    grade = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title


class StudentActivity(models.Model):
    student = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='activities')
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"{self.student.first_name} - {self.description}"

class News(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', default='Нет описания')
    image = models.ImageField(upload_to='media/news/', verbose_name='Фото', default='no-image.png')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

#Айжан, Манас нужна ли нам моделька Студент? Чтобыпри регистрации Родителя, у него точно был ребенок в этой школе?
class Student(models.Model):
    parent = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='children')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    grade = models.PositiveSmallIntegerField()
    avatar = models.ImageField(upload_to='media/child_avatar', blank=True, null=True)
    average_score = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

