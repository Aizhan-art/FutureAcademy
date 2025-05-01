from django.urls import path
from . import views

urlpatterns = [
    #это первая страница
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('student_activities/', views.StudentActivityListView.as_view(), name='student_activity_list'),
    path('children/', views.ChildrenListView.as_view(), name='children_list'),
    #новости
    path('news/', views.NewsListView.as_view(), name='news_list'),
    #достижения
    path('student-activities/', views.StudentActivityListView.as_view(), name='student_activity_list'),

    path('diary/', views.DiaryScheduleAPIView.as_view(), name='diary-schedule'),
    path('lessons/create/', views.LessonCreateAPIView.as_view(), name='lesson-create'),
    path('diary/create/', views.DiaryCreateAPIView.as_view(), name='diary-create'),
]
