from django.db import models
import datetime
from .choices import TaskStatusEnum, DiaryGradeEnum
from django.conf import settings

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

class StudentAchievement(models.Model):
    student = models.ForeignKey(MyUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    title = models.CharField(max_length=255)  
    date = models.DateField(auto_now_add=True)  
    is_victory = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.student.first_name} - {self.title}"

class Student(models.Model):
    parent = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='children')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    grade = models.PositiveSmallIntegerField()
    avatar = models.ImageField(upload_to='media/child_avatar', blank=True, null=True)
    average_score = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"




class Dashboard(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    projects_count = models.IntegerField(default=0)
    events_count = models.IntegerField(default=0)

    #def __str__(self):
     #   return f"Dashboard for {self.user}"



class Chat(models.Model):
   # users = models.ManyToManyField(User, through='ChatUser', related_name='chats')
    title = models.CharField(max_length=255)
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ChatUser(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    #def __str__(self):
     #   return f"{self.user} — {self.chat}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    #sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Новое поле для "Непрочитано/Прочитано"

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"



class LessonSchedule(models.Model):
    #teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons')  # преподаватель
    class_name = models.CharField(max_length=255)  # название класса или группы
    subject = models.CharField(max_length=255)  # предмет
    date = models.DateField(default=datetime.date.today)
    start_time = models.TimeField()  # начало урока
    end_time = models.TimeField()  # окончание урока


    def __str__(self):
        return f"{self.subject} for {self.class_name} by {self.teacher} on {self.date}"




class Diary(models.Model):
    #user = models.ForeignKey('MyUser', on_delete=models.CASCADE, related_name='diaries')
    lesson = models.ForeignKey(
        'LessonSchedule',
        on_delete=models.CASCADE,
        related_name='diaries',
        null=True,
        blank=True
    )
    title = models.CharField(max_length=255, verbose_name='Название записи')
    description = models.TextField(verbose_name='Описание записи')
    grade = models.IntegerField(choices=DiaryGradeEnum.choices, verbose_name='Оценка')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата записи')


    def __str__(self):
        return f"Diary Entry: {self.title} for {self.user}"



class Conversation(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Participant(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    #sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    #read_by = models.ManyToManyField(User, related_name='read_messages', blank=True)
