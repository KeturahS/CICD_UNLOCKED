# GitExercises/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('GitExercise1/', views.GitExercise1_view, name='git_quiz_1'),
]
