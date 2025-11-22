from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/profile/', views.manage_teacher_profile, name='teacher_profile'),
    path('teacher/schedules/', views.manage_schedules, name='teacher_schedules'),
    path('teacher/homework/', views.manage_homework, name='teacher_homework'),
    path('notification/mark-as-read/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('notification/clear-all', views.clear_all_notification, name="clear_all_notification"),
]
