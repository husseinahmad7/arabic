# from .models import UserLessonProgress

# def update_user_progress(*, user_id: int, lesson_id: int, completed_exercises: int, grade: float) -> UserLessonProgress:
#     progress, created = UserLessonProgress.objects.update_or_create(
#         user_id=user_id,
#         lesson_id=lesson_id,
#         defaults={
#             'completed_exercises': completed_exercises,
#             'grade': grade
#         }
#     )
#     return progress