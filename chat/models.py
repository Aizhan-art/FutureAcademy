from django.contrib.auth import get_user_model
from django.db import models

MyUser = get_user_model()


class Conversation(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Participant(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE, default=1)
    sender = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(MyUser, related_name='read_messages', blank=True)


    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"

#class Chat(models.Model):
#    users = models.ManyToManyField(MyUser, through='ChatUser', related_name='chats')
#    title = models.CharField(max_length=255)
#    is_group = models.BooleanField(default=False)
#    created_at = models.DateTimeField(auto_now_add=True)

#    def __str__(self):
#        return self.title


#class ChatUser(models.Model):
#    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
#    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

#    def __str__(self):
#        return f"{self.user} — {self.chat}"


#class Message(models.Model):
#    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
#    sender = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='sent_messages')
#    message = models.TextField()
#    timestamp = models.DateTimeField(auto_now_add=True)
#    is_read = models.BooleanField(default=False)  # Новое поле для "Непрочитано/Прочитано"

#    def __str__(self):
#        return f"Message from {self.sender} at {self.timestamp}"
