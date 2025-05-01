from rest_framework import serializers

from .models import  MyUser, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser

        fields = ['id', 'username', 'role']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message

        fields = ['id', 'sender', 'content', 'timestamp']


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation

        fields = ['id', 'name', 'is_group', 'created_at', 'messages', 'unread_count']

    def get_unread_count(self, obj):
        user = self.context['request'].user

        return obj.messages.exclude(read_by=user).count()
