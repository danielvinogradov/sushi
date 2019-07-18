from django.contrib.auth.decorators import login_required
from django.urls import path

from mickroservices import views

app_name = 'mickroservices'

urlpatterns = [
    path('faq/',
         login_required(views.QuestionView.as_view()),
         name='faq'),
    path('lessons/',
         login_required(views.CoursesView.as_view()),
         name='lessons'),
    path('lesson/<int:pk>',
         login_required(views.CourseView.as_view()),
         name='lesson'),
    path('news/',
         login_required(views.NewsView.as_view()),
         name='news'),
    path('marketing/',
         login_required(views.MarketingView.as_view()),
         name='marketing'),
    path('schedule/<int:pk>',
         login_required(views.ScheduleView.as_view()),
         name='schedule_view'),
    path('schedule/create/',
         login_required(views.ScheduleCreateView.as_view()),
         name='schedule_new'),
    path('schedule/<int:pk>',
         login_required(views.ScheduleView.as_view()),
         name='schedule_edit'),
    path('schedule/',
         login_required(views.ScheduleListView.as_view()),
         name='schedule'),
]
