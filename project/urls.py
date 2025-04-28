from django.urls import path
from .views import ConversationListCreateAPIView, MessageListCreateAPIView, MarkMessagesReadAPIView

urlpatterns = [
<<<<<<< HEAD
    path('api/diary-schedule/', views.DiaryScheduleAPIView.as_view(), name='diary-schedule'),

=======
    path('conversations/', ConversationListCreateAPIView.as_view(), name='conversation-list-create'),
    path('conversations/<int:conversation_id>/messages/', MessageListCreateAPIView.as_view(), name='message-list-create'),
    path('conversations/<int:conversation_id>/mark_read/', MarkMessagesReadAPIView.as_view(), name='mark-messages-read'),
>>>>>>> 0b3e1ee079c0d040068d9431572f401772ac59f1
]