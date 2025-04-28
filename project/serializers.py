from rest_framework import serializers
from .models import LessonSchedule, Diary

class LessonWithGradeSerializer(serializers.ModelSerializer):
    grade = serializers.SerializerMethodField()

    class Meta:
        model = LessonSchedule
        fields = ('subject', 'start_time', 'end_time', 'grade')

    def get_grade(self, obj):
        user = self.context.get('user')
        diary = Diary.objects.filter(user=user, lesson=obj).first()
        return diary.grade if diary else None
