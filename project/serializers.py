from rest_framework import serializers
from .models import LessonSchedule, Diary
from rest_framework import serializers
from .models import Project, Task, Event, StudentActivity, News, StudentAchievement
from django.contrib.auth import get_user_model
from .models import MyUser

class LessonWithGradeSerializer(serializers.ModelSerializer):
    grade = serializers.SerializerMethodField()

    class Meta:
        model = LessonSchedule
        fields = ('subject', 'start_time', 'end_time', 'grade')

    def get_grade(self, obj):
        user = self.context.get('user')
        diary = Diary.objects.filter(user=user, lesson=obj).first()
        return diary.grade if diary else None



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'grade', 'avatar', 'average_score']
        
class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'first_name', 'last_name', 'grade', 'avatar', 'average_score']

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


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'description', 'image', 'created_at']

class StudentAchievementSummarySerializer(serializers.ModelSerializer):
    last_achievement = serializers.SerializerMethodField()
    total_participations = serializers.SerializerMethodField()
    total_victories = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ['id', 'first_name', 'last_name', 'grade', 'last_achievement', 'total_participations', 'total_victories']

    def get_last_achievement(self, obj):
        achievement = StudentAchievement.objects.filter(student=obj).order_by('-date').first()
        return achievement.title if achievement else None

    def get_total_participations(self, obj):
        return StudentAchievement.objects.filter(student=obj).count()

    def get_total_victories(self, obj):
        return StudentAchievement.objects.filter(student=obj, is_victory=True).count()

