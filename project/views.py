<<<<<<< HEAD
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LessonSchedule
from .serializers import LessonWithGradeSerializer
import calendar


class DiaryScheduleAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user  # текущий пользователь
        lessons = LessonSchedule.objects.filter(teacher=user)  # фильтруем по учителю
        serializer = LessonWithGradeSerializer(lessons, many=True, context={'user': user})

        data = {}
        for lesson_data in serializer.data:
            date_obj = lessons.get(subject=lesson_data['subject'], start_time=lesson_data['start_time']).date
            weekday = calendar.day_name[
                date_obj.weekday()]  # Получаем название дня недели на английском (например, Monday)

            # Перевод на русский
            week_translation = {
                'Monday': 'Понедельник',
                'Tuesday': 'Вторник',
                'Wednesday': 'Среда',
                'Thursday': 'Четверг',
                'Friday': 'Пятница',
                'Saturday': 'Суббота',
                'Sunday': 'Воскресенье',
            }
            day_name = week_translation.get(weekday, weekday)

            if day_name not in data:
                data[day_name] = []

            data[day_name].append({
                'title': lesson_data['subject'],
                'start_time': lesson_data['start_time'],
                'end_time': lesson_data['end_time'],
                'grade': lesson_data['grade']
            })

        return Response(data)

=======
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participant__user=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participant_set.create(user=self.request.user)

class MessageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        return Message.objects.filter(conversation_id=conversation_id)

    def perform_create(self, serializer):
        conversation_id = self.kwargs['conversation_id']
        serializer.save(sender=self.request.user, conversation_id=conversation_id)

class MarkMessagesReadAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, conversation_id):
        conversation = Conversation.objects.get(id=conversation_id)
        messages = conversation.messages.exclude(read_by=request.user)
        for message in messages:
            message.read_by.add(request.user)
        return Response({"status": "messages marked as read"})
>>>>>>> 0b3e1ee079c0d040068d9431572f401772ac59f1
