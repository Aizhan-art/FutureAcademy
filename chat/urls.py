from django.urls import path
from . import views


urlpatterns = [

    path('conversations/', views.ConversationListCreateAPIView.as_view(), name='conversation-list-create'),

    path('conversations/<int:conversation_id>/messages/', views.MessageListCreateAPIView.as_view(),
         name='message-list-create'),

    path('conversations/<int:conversation_id>/mark_read/', views.MarkMessagesReadAPIView.as_view(),
         name='mark-messages-read'),
]