from django.db import models
from django.contrib.auth.models import User

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.title

class Vocabulary(models.Model):
    word = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)
    image = models.ImageField(upload_to='vocabulary_images/', null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return self.word

# class UserProgress(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
#     completed = models.BooleanField(default=False)
#     score = models.IntegerField(default=0)

#     class Meta:
#         unique_together = ('user', 'lesson')

# class Exercise(models.Model):
#     lesson = models.ForeignKey(Lesson, related_name='exercises', on_delete=models.CASCADE,null=True)
#     order = models.IntegerField(null=True)
#     question = models.CharField(max_length=200)
#     correct_answer = models.CharField(max_length=200)
#     image = models.ImageField(upload_to='exercise_images/', null=True, blank=True)

#     class Meta:
#         unique_together = ['lesson', 'order']
#         ordering = ['order']

#     def __str__(self):
#         return f"{self.lesson.title} - Exercise {self.order}"
class Exercise(models.Model):
    EXERCISE_TYPES = (
        ('WS', 'Written and Spoken'),
        ('FE', 'Fill Empty'),
        ('PL', 'Plural'),
        ('NW', 'New Way'),
    )
    lesson = models.ForeignKey(Lesson, related_name='exercises', on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=EXERCISE_TYPES)
    order = models.IntegerField()

    class Meta:
        unique_together = ['lesson', 'order']
        ordering = ['order']

    def __str__(self):
        return f"{self.lesson.title} - Exercise {self.order}"

class Exercise(models.Model):
    EXERCISE_TYPES = (
        ('WRITTEN_SPOKEN', 'Written and Spoken'),
        ('FILL_BLANKS', 'Fill the Blanks'),
        ('TRANSFORM', 'Transform Phrase'),
    )
    lesson = models.ForeignKey(Lesson, related_name='exercises', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=EXERCISE_TYPES)
    order = models.IntegerField()

    class Meta:
        unique_together = ['lesson', 'order']
        ordering = ['order']

    def __str__(self):
        return f"{self.lesson.title} - Exercise {self.order}"

class Question(models.Model):
    exercise = models.ForeignKey(Exercise, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    correct_answer = models.TextField()
    order = models.IntegerField()
    image = models.ImageField(upload_to='exercise_images/', null=True, blank=True)

    class Meta:
        unique_together = ['exercise', 'order']
        ordering = ['order']

    def __str__(self):
        return f"{self.exercise} - Question {self.order}"

class UserExerciseProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    last_attempted_question = models.IntegerField(default=0)

    class Meta:
        unique_together = ['user', 'exercise']

class UserQuestionAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    written_attempt = models.TextField(blank=True, null=True)
    spoken_attempt = models.TextField(blank=True, null=True)
    is_correct = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'question']

# class ExerciseOption(models.Model):
#     exercise = models.ForeignKey(Exercise, related_name='options', on_delete=models.CASCADE)
#     text = models.CharField(max_length=200)
#     is_correct = models.BooleanField(default=False)

#     def __str__(self):
#         return self.text

# class UserExerciseAttempt(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
#     written_attempt = models.CharField(max_length=200, blank=True, null=True)
#     spoken_attempt = models.CharField(max_length=200, blank=True, null=True)
#     is_correct = models.BooleanField(default=False)
#     timestamp = models.DateTimeField(auto_now_add=True)

# class UserLessonProgress(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
#     completed_exercises = models.IntegerField(default=0)
#     total_exercises = models.IntegerField()
#     grade = models.FloatField(default=0.0)

#     class Meta:
#         unique_together = ['user', 'lesson']