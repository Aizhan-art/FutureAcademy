from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Project, Task, Event, StudentActivity, News, Student
from django.contrib.auth import get_user_model
from django.db.models import Q
from .permissions import OnlyReadForParentsPermission

from .serializers import (
    ProjectSerializer, EventSerializer, StudentActivitySerializer, StudentSerializer, NewsSerializer)

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
    permission_classes = [OnlyReadForParentsPermission]
    def get(self, request):
        children = MyUser.objects.filter(role=False, grade__isnull=False)
        activities = StudentActivity.objects.filter(student__in=children).order_by('-date')[:10]
        serializer = StudentActivitySerializer(activities, many=True)
        return Response(serializer.data)


class ChildrenListView(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [OnlyReadForParentsPermission]
    def get(self, request):
        children = MyUser.objects.filter(role=False, grade__isnull=False)
        serializer = StudentSerializer(children, many=True)
        return Response(serializer.data)

#Все надо оформлять так или как выше отдельно?
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Последние 3 проекта
        projects = Project.objects.all().order_by('-created_at')[:3]
        projects_serializer = ProjectSerializer(projects, many=True)

        # Последние 3 мероприятия
        events = Event.objects.all().order_by('-start_date')[:3]
        events_serializer = EventSerializer(events, many=True)

        # Последние 3 события детей пользователя
        student_activities = StudentActivity.objects.filter(child__parent=request.user).order_by('-date')[:3]
        student_activity_serializer = StudentActivitySerializer(student_activities, many=True)

        # Все дети родителя
        students = Student.objects.filter(parent=request.user)
        student_serializer = StudentSerializer(students, many=True)

        return Response({
            "projects": projects_serializer.data,
            "events": events_serializer.data,
            "student_activity": student_activity_serializer.data,
            "student_serializer": student_serializer.data,
        })

class NewsListView(APIView):
    permission_classes = [IsAuthenticated]

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

class OnlyReadForParentsPermission(IsAuthenticated):
    def has_permission(self, request, view):

        if request.user.role == 'parent':
            return request.method in ('GET', 'HEAD', 'OPTIONS')
        return True