from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from django.shortcuts import get_object_or_404
from .models import (Project, Task, Event, StudentActivity, News, StudentAchievement,
                     Student, Dashboard, LessonSchedule, Diary)
from django.contrib.auth import get_user_model
from django.db.models import Q

from .permissions import OnlyReadForParentsPermission
from rest_framework.generics import CreateAPIView
from django.utils.timezone import now
from datetime import timedelta
from .serializers import (ProjectSerializer, EventSerializer, StudentActivitySerializer,
                          NewsSerializer,StudentAchievementSummarySerializer, ChildSerializer,
                          LessonWithGradeSerializer, LessonSerializer, DiarySerializer)


MyUser = get_user_model()

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

class DiaryScheduleAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        data = {}

        if user.role == 'teacher':
            lessons = LessonSchedule.objects.filter(teacher=user)
        elif user.role in ['student', 'parent']:
            lessons = LessonSchedule.objects.filter(class_name=user.class_name)
        else:
            return Response({'ошибка': 'Недостаточно прав'}, status=403)

        # неделя и диапазон дат
        week_param = int(request.query_params.get('week', 1))
        today = now().date()
        monday = today - timedelta(days=today.weekday()) + timedelta(weeks=week_param - 1)
        friday = monday + timedelta(days=4)

        lessons = lessons.filter(date__range=(monday, friday)).order_by('date', 'start_time')

        serializer = LessonWithGradeSerializer(lessons, many=True, context={'user': user})

        # группируем по дате
        for lesson_data in serializer.data:
            lesson_obj = lessons.get(subject=lesson_data['subject'], start_time=lesson_data['start_time'])
            date_str = lesson_obj.date.strftime('%d.%m.%Y')

            if date_str not in data:
                data[date_str] = []

            data[date_str].append({
                'предмет': lesson_data['subject'],
                'время_начала': lesson_data['start_time'],
                'время_окончания': lesson_data['end_time'],
                'оценка': lesson_data['grade']
            })

        return Response(data)


class LessonCreateAPIView(CreateAPIView):
    queryset = LessonSchedule.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser]


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'teacher'


class DiaryCreateAPIView(CreateAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [IsTeacher]
