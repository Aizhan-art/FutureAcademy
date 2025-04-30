from django.urls import path
from . import views

urlpatterns = [
    path('api/diary-schedule/', views.DiaryScheduleAPIView.as_view(), name='diary-schedule'),
    
    #это первая страница
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('events/', EventListView.as_view(), name='event_list'),
    path('student_activities/', StudentActivityListView.as_view(), name='student_activity_list'),
    path('children/', ChildrenListView.as_view(), name='children_list'),
    #новости
    path('news/', NewsListView.as_view(), name='news_list'),
    #достижения
    path('student-activities/', StudentActivityListView.as_view(), name='student_activity_list'),
]
