from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LessonSchedule
from .serializers import LessonWithGradeSerializer
import calendar
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Project, Task, Event, StudentActivity, News, Student
from django.contrib.auth import get_user_model
from django.db.models import Q
from .permissions import OnlyReadForParentsPermission

from .serializers import (
    ProjectSerializer, EventSerializer, StudentActivitySerializer, NewsSerializer,
    StudentAchievementSummarySerializer, ChildSerializer)

MyUser = get_user_model()

class DiaryScheduleAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user

        data = {}

        # Проверяем роль пользователя
        if user.role == 'teacher':
            lessons = LessonSchedule.objects.filter(teacher=user)

        elif user.role in ['student', 'parent']:
            # Если ученик или родитель, берем все уроки класса ученика
            lessons = LessonSchedule.objects.filter(class_name=user.class_name)

        else:
            return Response({'error': 'Недостаточно прав'}, status=403)

        # Сериализация уроков
        serializer = LessonWithGradeSerializer(lessons, many=True, context={'user': user})

        for lesson_data in serializer.data:
            # Находим день недели
            lesson_obj = lessons.get(subject=lesson_data['subject'], start_time=lesson_data['start_time'])
            date_obj = lesson_obj.date

            weekday = calendar.day_name[date_obj.weekday()]  # Получаем день недели на английском

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




class ProjectListView(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [OnlyReadForParentsPermission]

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class EventListView(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [OnlyReadForParentsPermission]

    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class StudentActivityListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role == 'parent':
            children = MyUser.objects.filter(parent=request.user, role='student')
            activities = StudentActivity.objects.filter(student__in=children).order_by('-date')[:3]

        elif request.user.role == 'student':
            activities = StudentActivity.objects.filter(student=request.user).order_by('-date')[:3]
        else:
            return Response({'detail': 'Access denied'}, status=403)

        serializer = StudentActivitySerializer(activities, many=True)
        return Response(serializer.data)

class ChildrenListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'parent':
            return Response({'detail': 'Only parents can view children'}, status=403)

        children = MyUser.objects.filter(parent=request.user, role='student')
        serializer = ChildSerializer(children, many=True)
        return Response(serializer.data)

class NewsListView(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [OnlyReadForParentsPermission]

    def get(self, request):
        search_query = request.query_params.get('search', '')
        news = News.objects.all()

        if search_query:
            news = news.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        news = news.order_by('-created_at')
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)


class StudentAchievementListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'parent':
            return Response({'detail': 'Only parents can view student achievements'}, status=403)

        children = MyUser.objects.filter(parent=request.user, role='student')
        serializer = StudentAchievementSummarySerializer(children, many=True)
        return Response(serializer.data)
