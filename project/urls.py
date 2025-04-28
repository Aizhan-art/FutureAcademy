from django.urls import path
from .views import ConversationListCreateAPIView, MessageListCreateAPIView, MarkMessagesReadAPIView

urlpatterns = [
    path('conversations/', ConversationListCreateAPIView.as_view(), name='conversation-list-create'),
    path('conversations/<int:conversation_id>/messages/', MessageListCreateAPIView.as_view(), name='message-list-create'),
    path('conversations/<int:conversation_id>/mark_read/', MarkMessagesReadAPIView.as_view(), name='mark-messages-read'),
]