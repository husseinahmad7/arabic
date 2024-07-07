from django.contrib import admin
from .models import Lesson, Exercise, Question,UserExerciseProgress,UserQuestionAttempt

admin.site.register(Lesson)
admin.site.register(Exercise)
admin.site.register(Question)
admin.site.register(UserExerciseProgress)
admin.site.register(UserQuestionAttempt)
