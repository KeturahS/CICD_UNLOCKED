# GitExercises/views.py
from django.shortcuts import render

def GitExercise1_view(request):
    return render(request, 'GitExercises/section1_questions.html')


# Create your views here.
