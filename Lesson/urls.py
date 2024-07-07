from django.urls import path
from . import views

# urlpatterns = [
#     path('', views.lesson_list, name='lesson_list'),
#     # path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
# ] + [
#     path('exercise/', views.exercise_view, name='exercise'),
#     path('check-answer/', views.check_answer, name='check_answer'),
#     path('exercise/<int:exercise_id>/check-handwritten/', views.check_handwritten, name='check_handwritten'),

# ]

# urlpatterns = [
#     path('lessons/', views.LessonListApi.as_view(), name='lesson-list'),
#     path('lessons/<int:lesson_id>/', views.LessonDetailApi.as_view(), name='lesson-detail'),
#     path('progress/', views.UserLessonProgressApi.as_view(), name='user-progress'),
# ]
urlpatterns = [
    path('lessons/', views.LessonListView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', views.LessonRetrieveView.as_view(), name='lesson-detail'),
    path('lessons/<int:lesson_id>/exercises/', views.ExerciseListView.as_view(), name='exercise-list'),
    path('exercises/<int:exercise_id>/questions/', views.QuestionListView.as_view(), name='question-list'),
    path('check-answer/', views.CheckAnswerView.as_view(), name='check-answer'),
    path('progress/<int:exercise_id>/', views.UserProgressView.as_view(), name='user-progress'),
]