from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Lesson, Vocabulary, Exercise#, ExerciseOption #,UserLessonProgress
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import cv2
# import numpy as np
# import pytesseract
# from PIL import Image
# import io
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Lesson,Question,UserExerciseProgress, UserQuestionAttempt #UserLessonProgress
# from .serializers import LessonSerializer, UserLessonProgressSerializer
# from .selectors import get_lessons, get_lesson, get_user_progress

# from .services import update_user_progress


class VocabularySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocabulary
        fields = ['id', 'word', 'translation', 'image']

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    vocabulary = VocabularySerializer(many=True, read_only=True)
    # exercises = ExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'order', 'vocabulary']#, 'exercises']

# class UserLessonProgressSerializer(serializers.ModelSerializer):
#     lesson = LessonSerializer(read_only=True)

#     class Meta:
#         model = UserLessonProgress
#         fields = ['id', 'lesson', 'completed_exercises', 'total_exercises', 'grade']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class UserExerciseProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExerciseProgress
        fields = '__all__'
        

class LessonListView(generics.ListAPIView):
    queryset = Lesson.objects.all().order_by('order')
    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated]

class LessonRetrieveView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class ExerciseListView(generics.ListAPIView):
    serializer_class = ExerciseSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lesson_id = self.kwargs['lesson_id']
        return Exercise.objects.filter(lesson_id=lesson_id).order_by('order')

class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        exercise_id = self.kwargs['exercise_id']
        return Question.objects.filter(exercise_id=exercise_id).order_by('order')

class CheckAnswerView(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        question_id = request.data.get('question_id')
        written_answer = request.data.get('written_answer', '')
        spoken_answer = request.data.get('spoken_answer', '')

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

        is_correct = (written_answer.strip('., ').lower() == question.correct_answer.lower() or
                      spoken_answer.strip('., ').lower() == question.correct_answer.lower())

        # UserQuestionAttempt.objects.update_or_create(
        #     user=request.user,
        #     question=question,
        #     defaults={
        #         'written_attempt': written_answer,
        #         'spoken_attempt': spoken_answer,
        #         'is_correct': is_correct
        #     }
        # )

        # progress, _ = UserExerciseProgress.objects.get_or_create(
        #     user=request.user,
        #     exercise=question.exercise
        # )
        
        # if is_correct:
        #     progress.last_attempted_question = question.order
        #     if progress.last_attempted_question == question.exercise.questions.count():
        #         progress.is_completed = True
        #     progress.save()

        return Response({'is_correct': is_correct})

class UserProgressView(generics.RetrieveAPIView):
    serializer_class = UserExerciseProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        exercise_id = self.kwargs['exercise_id']
        return UserExerciseProgress.objects.get_or_create(
            user=self.request.user,
            exercise_id=exercise_id
        )[0]
# class LessonListApi(generics.ListAPIView):
#     # permission_classes = [IsAuthenticated]
#     serializer_class = LessonSerializer

#     def get_queryset(self):
#         return get_lessons()

# class LessonDetailApi(generics.RetrieveAPIView):
#     # permission_classes = [IsAuthenticated]

#     def get(self, request, lesson_id):
#         try:
#             lesson = get_lesson(lesson_id=lesson_id)
#         except Lesson.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         serializer = LessonSerializer(lesson)
#         return Response(serializer.data)

# class UserLessonProgressApi(generics.RetrieveAPIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         progress = get_user_progress(user_id=request.user.id)
#         serializer = UserLessonProgressSerializer(progress, many=True)
#         return Response(serializer.data)

# class UpdateUserProgressApi(generics.UpdateAPIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         lesson_id = request.data.get('lesson_id')
#         completed_exercises = request.data.get('completed_exercises')
#         grade = request.data.get('grade')

#         if not all([lesson_id, completed_exercises, grade]):
#             return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

#         progress = update_user_progress(
#             user_id=request.user.id,
#             lesson_id=lesson_id,
#             completed_exercises=completed_exercises,
#             grade=grade
#         )

#         serializer = UserLessonProgressSerializer(progress)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# @login_required
# def lesson_list(request):
#     lessons = Lesson.objects.all().order_by('order')
#     return render(request, 'lessons/lesson_list.html', {'lessons': lessons})

# @login_required
# def lesson_detail(request, lesson_id):
#     lesson = get_object_or_404(Lesson, id=lesson_id)
#     vocabulary = Vocabulary.objects.filter(lesson=lesson)
#     # progress, created = UserProgress.objects.get_or_create(user=request.user, lesson=lesson)
    
#     progress, created = UserLessonProgress.objects.get_or_create(
#         user=request.user, 
#         lesson=lesson,
#         defaults={'total_exercises': lesson.exercises.count()}
#     )
#     return render(request, 'lessons/lesson_detail.html', {'lesson': lesson,'vocabulary': vocabulary, 'progress': progress})




def exercise_view(request):
    exercise = Exercise.objects.order_by('?').first()  # Get a random exercise
    # options = exercise.options.all() if exercise.type == 'IDENTIFY' else None
    return render(request, 'lessons\exercise.html', {'exercise': exercise})#, 'options': options})

def check_answer(request):
    if request.method == 'POST':
        exercise_id = request.POST.get('exercise_id')
        user_answer = request.POST.get('answer')
        exercise = Exercise.objects.get(id=exercise_id)
        is_correct = user_answer.strip('., ').lower() == exercise.correct_answer.lower()
        return JsonResponse({'is_correct': is_correct})



# def preprocess_and_ocr(image):
#     # Convert to grayscale if not already
#     if len(image.shape) == 3:
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     else:
#         gray = image

#     # Increase contrast
#     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
#     contrast = clahe.apply(gray)

#     # Apply adaptive thresholding
#     binary = cv2.adaptiveThreshold(contrast, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

#     # Dilate to thicken text
#     kernel = np.ones((2,2),np.uint8)
#     dilated = cv2.dilate(binary, kernel, iterations=1)

#     # Invert back
#     # inverted = cv2.bitwise_not(dilated)

#     # # Perform OCR
#     # text1 = pytesseract.image_to_string(inverted, lang='ara', config='--psm 6')
    
#     # Try another preprocessing method
#     _, otsu = cv2.threshold(contrast, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#     text2 = pytesseract.image_to_string(otsu, lang='ara', config='--psm 6')

#     # Combine results
#     combined_text = text2
#     return combined_text.strip()

# def enhance_thin_lines(image):
#     # Convert to grayscale if not already
#     if len(image.shape) == 3:
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     else:
#         gray = image

#     # Increase contrast
#     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
#     contrast = clahe.apply(gray)

#     # Sharpen the image
#     kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
#     sharpened = cv2.filter2D(contrast, -1, kernel)

#     # Binarize the image
#     _, binary = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

#     # Dilate to thicken lines
#     kernel = np.ones((2,2),np.uint8)
#     dilated = cv2.dilate(binary, kernel, iterations=1)

#     # Remove noise
#     denoised = cv2.medianBlur(dilated, 3)

#     return denoised


# def enhance_image(image):
#     # Convert to grayscale if not already
#     if len(image.shape) == 3:
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     else:
#         gray = image

#     # Increase contrast
#     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
#     contrast = clahe.apply(gray)

#     # Denoise
#     denoised = cv2.fastNlMeansDenoising(contrast, None, 10, 7, 21)

#     # Sharpen the image
#     kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
#     sharpened = cv2.filter2D(denoised, -1, kernel)

#     # Binarize the image
#     _, binary = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

#     return binary

# @csrf_exempt
# def check_handwritten(request, exercise_id):
#     if request.method == 'POST' and request.FILES.get('image'):
#         exercise = get_object_or_404(Exercise, id=exercise_id)
        
#         # Read the image file
#         image_file = request.FILES['image']
#         image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
        
#         # Preprocess the image
#         # image = cv2.resize(image, (320, 240))  # Resize to 320x240
#         # image = cv2.GaussianBlur(image, (5, 5), 0)  # Apply Gaussian blur
#         # _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Apply thresholding
        

#         # Ensure the image is 640x640
#         image = cv2.resize(image, (640, 640))
#         # image = cv2.GaussianBlur(image, (5, 5), 0)  # Apply Gaussian blur
#         _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Apply thresholding
        
#         # Enhance the image
#         enhanced = enhance_image(image)
#         # Convert OpenCV image to PIL Image
#         image = enhance_thin_lines(enhanced)
#         pil_image = Image.fromarray(enhanced)

#         config = f'--psm 1'
#         # Perform OCR
#         extracted_text = pytesseract.image_to_string(pil_image, lang='ara',config=config)
#         # extracted_text = preprocess_and_ocr(image)
#         print(extracted_text)
        
#         # Clean up the extracted text
#         extracted_text = extracted_text.strip().lower()
        
#         # Check if the answer is correct
#         is_correct = extracted_text == exercise.correct_answer.lower()
        
#         return JsonResponse({'is_correct': is_correct, 'extracted_text': extracted_text})
    
#     return JsonResponse({'error': 'Invalid request'}, status=400)