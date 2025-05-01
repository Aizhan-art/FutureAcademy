
from django.urls import path
from .views import ChatListAPIView, ChatDetailAPIView, SendMessageAPIView

urlpatterns = [
    path('chats/', ChatListAPIView.as_view(), name='chat-list'),
    path('chats/<int:chat_id>/', ChatDetailAPIView.as_view(), name='chat-detail'),
    path('chats/<int:chat_id>/send/', SendMessageAPIView.as_view(), name='send-message'),
]


