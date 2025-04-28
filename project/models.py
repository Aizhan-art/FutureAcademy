from django.db import models
from .choices import TaskStatusEnum, DiaryGradeEnum


class Image(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='images')
    file = models.ImageField(upload_to='media/projects/detail_image')
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.file)

#  TODO: Добавить связь с юзером
class Project(models.Model):
    # user = modes.(Fo....)
    title = models.CharField(max_length=225, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    main_cover = models.ImageField(upload_to='media/projects/main_cover', verbose_name='Главное фото')
    created_at = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

#  TODO: Добавить связь с юзером
class UserProject(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    #def __str__(self):
       # return f"{self.user} — {self.project}"


#  TODO: Добавить связь с юзером
class Event(models.Model):
    #users = models.ManyToManyField(User, through='UserEvent', related_name='events')
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    grade = models.IntegerField()  # или models.CharField, если уровни разные


    def __str__(self):
        return self.title


#  TODO: Добавить связь с юзером
class UserEvent(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    #def __str__(self):
     #   return f"{self.user} — {self.event}"


#  TODO: Добавить связь с юзером
class Classmate(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=255)
    graduation_year = models.IntegerField()

    #def __str__(self):
     #   return f"{self.user} — {self.class_name}"


#  TODO: Добавить связь с юзером
class Employee(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    hire_date = models.DateField()

    #def __str__(self):
     #   return f"{self.user} — {self.position}"

#  TODO: Добавить связь с юзером
class News(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

#  TODO: Добавить связь с юзером
class Dashboard(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    projects_count = models.IntegerField(default=0)
    events_count = models.IntegerField(default=0)

    #def __str__(self):
     #   return f"Dashboard for {self.user}"



#  TODO: Добавить связь с юзером
class Chat(models.Model):
    title = models.CharField(max_length=255)
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    #users = models.ManyToManyField(User, through='ChatUser', related_name='chats')

    def __str__(self):
        return self.title

#  TODO: Добавить связь с юзером
class ChatUser(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

   # def __str__(self):
    #    return f"{self.user} — {self.chat}"

#  TODO: Добавить связь с юзером
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    #sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Новое поле для "Непрочитано/Прочитано"

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"



#  TODO: Добавить связь с юзером
class LessonSchedule(models.Model):
    #teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons')  # преподаватель
    class_name = models.CharField(max_length=255)  # название класса или группы
    subject = models.CharField(max_length=255)  # предмет
    start_time = models.DateTimeField()  # начало урока
    end_time = models.DateTimeField()  # окончание урока

    def __str__(self):
        return f"{self.subject} for {self.class_name} by {self.teacher}"

#  TODO: Добавить связь с юзером
class Task(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='tasks')
    #user = models.ForeignKey('MyUser', on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255, verbose_name='Название задачи')
    description = models.TextField(verbose_name='Описание задачи')
    status = models.CharField(
        max_length=50,
        choices=TaskStatusEnum.choices,
        default=TaskStatusEnum.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"Task: {self.title}"


#  TODO: Добавить связь с юзером
class Diary(models.Model):
    #user = models.ForeignKey('MyUser', on_delete=models.CASCADE, related_name='diaries')
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(User, related_name='read_messages', blank=True)