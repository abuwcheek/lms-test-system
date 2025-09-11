from django.urls import path
from .views import StartExamView, QuestionView, FinishExamView, ReviewExamView

app_name = 'exam'

urlpatterns = [
     path('start/', StartExamView.as_view(), name='start'),
     path('question/<int:question_index>/', QuestionView.as_view(), name='question'),
     path('finish/', FinishExamView.as_view(), name='finish'),
     path('review/', ReviewExamView.as_view(), name='review'),
]
