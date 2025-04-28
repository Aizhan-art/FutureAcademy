from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LessonSchedule
from .serializers import LessonWithGradeSerializer
import calendar


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

