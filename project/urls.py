from django.urls import path
from . import views

urlpatterns = [
    path('api/diary-schedule/', views.DiaryScheduleAPIView.as_view(), name='diary-schedule'),

]