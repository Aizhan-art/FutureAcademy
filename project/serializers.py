from rest_framework import serializers
from .models import Project, Task, Event, StudentActivity, News
from django.contrib.auth import get_user_model

MyUser = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'is_active', 'responsible_user']


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'main_cover', 'deadline', 'tasks']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'start_date', 'end_date', 'grade']


class StudentActivitySerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.first_name', read_only=True)

    class Meta:
        model = StudentActivity
        fields = ['id', 'student_name', 'description', 'date']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'first_name', 'last_name', 'avatar', 'grade']



class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'description', 'image', 'created_at']