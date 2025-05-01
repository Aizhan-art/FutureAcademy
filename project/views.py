
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils.timezone import localtime
from rest_framework import status
from .serializers import ChatPreviewSerializer, SendMessageSerializer, MessageDetailSerializer

from .models import Chat, ChatUser, Message

class ChatListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        chats = Chat.objects.filter(chatuser__user=user).distinct()

        public_chats = []
        personal_chats = []

        for chat in chats:
            last_message = chat.messages.order_by('-timestamp').first()
            unread_count = chat.messages.filter(is_read=False).exclude(sender=user).count()

            chat_data = {
                "id": chat.id,
                "title": chat.title,
                "logo": chat.logo.url if chat.logo else "",  # or static placeholder
                "last_message": last_message.message if last_message else "",
                "total_unread_messages": unread_count,
                "last_message_time": localtime(last_message.timestamp).strftime("%H:%M") if last_message else "",
                "is_read": unread_count == 0
            }

            if chat.is_group:
                public_chats.append(chat_data)
            else:
                personal_chats.append(chat_data)

        return Response({
            "public_chat": public_chats,
            "personal_chat": personal_chats
        })

class ChatDetailAPIView(APIView):
        permission_classes = [IsAuthenticated]

        def get(self, request, chat_id):
            user = request.user
            chat = get_object_or_404(Chat, id=chat_id)

            messages = chat.messages.order_by('timestamp')

            serialized_messages = []

            for msg in messages:
                serialized_messages.append({
                    "id": msg.id,
                    "username": msg.sender.username,
                    "user_logo": msg.sender.profile_image.url if msg.sender.profile_image else "",
                    "sent_at": localtime(msg.timestamp).strftime("%Y.%m.%d"),
                    "message": msg.message,
                    "is_current_user": msg.sender == user
                })

                # Optionally mark as read
                if msg.sender != user and not msg.is_read:
                    msg.is_read = True
                    msg.save()

            return Response({
                "id": chat.id,
                "title": chat.title,
                "logo": chat.logo.url if chat.logo else "",
                "messages": serialized_messages
            })

class SendMessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id)

        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message_text = serializer.validated_data['message']

        # Create the message
        message = Message.objects.create(
            chat=chat,
            sender=request.user,
            message=message_text
        )

        # Prepare response data
        response_data = {
            "id": message.id,
            "username": request.user.username,
            "user_logo": request.user.profile_image.url if request.user.profile_image else "",
            "sent_at": localtime(message.timestamp).strftime("%Y.%m.%d"),
            "message": message.message,
            "is_current_user": True
        }

        return Response(response_data, status=status.HTTP_201_CREATED)