from django.db.models import Prefetch
from .models import Lesson, Vocabulary, Exercise#, UserLessonProgress

def get_lessons():
    return Lesson.objects.all().order_by('order').prefetch_related(
        # Prefetch('vocabulary_set', queryset=Vocabulary.objects.all(), to_attr='vocabulary'),
        Prefetch('exercises', queryset=Exercise.objects.all().order_by('order'))
    )

def get_lesson(*, lesson_id: int):
    return Lesson.objects.prefetch_related(
        Prefetch('vocabulary_set', queryset=Vocabulary.objects.all(), to_attr='vocabulary'),
        Prefetch('exercises', queryset=Exercise.objects.all().order_by('order'))
    ).get(id=lesson_id)

# def get_user_progress(*, user_id: int):
#     return UserLessonProgress.objects.filter(user_id=user_id).select_related('lesson')