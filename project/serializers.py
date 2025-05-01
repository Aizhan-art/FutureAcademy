from rest_framework import serializers
from .models import User, Conversation, Message
from django.utils.timezone import localtime


class ChatPreviewSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    logo = serializers.CharField()  # You can use serializers.ImageField() if serving images
    last_message = serializers.CharField()
    total_unread_messages = serializers.IntegerField()
    last_message_time = serializers.CharField()
    is_read = serializers.BooleanField()

class MessageDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    user_logo = serializers.CharField()
    sent_at = serializers.CharField()
    message = serializers.CharField()
    is_current_user = serializers.BooleanField()

class SendMessageSerializer(serializers.Serializer):
    message = serializers.CharField()