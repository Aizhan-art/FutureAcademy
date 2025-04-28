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

