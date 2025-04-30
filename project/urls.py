from django.urls import path
from .views import ProjectListView, EventListView, StudentActivityListView, ChildrenListView, NewsListView

urlpatterns = [

    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('events/', EventListView.as_view(), name='event_list'),
    path('student_activities/', StudentActivityListView.as_view(), name='student_activity_list'),
    path('children/', ChildrenListView.as_view(), name='children_list'),

    path('news/', NewsListView.as_view(), name='news_list'),
]