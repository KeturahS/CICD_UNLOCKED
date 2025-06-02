# GitExercises/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('GitExercise1/', views.GitExercise1_view, name='git_quiz_1'),
    path('GitScenarioExercise/', views.GitScenarioExercise, name='GitScenarioExercise'),
    path('update-command-status/', views.update_command_status, name='update_command_status'),
    path('update-command-attempts-status/', views.update_command_attempts_status, name='update_command_attempts_status'),
    path('update_jenkins_quiz_completion/', views.update_jenkins_quiz_completion,
         name='update_jenkins_quiz_completion'),

    path('jenkins/questions/', views.jenkins_questions_view, name='jenkins_questions'),
    path('jenkins/submit/', views.handle_pipeline_submission, name='handle_pipeline_submission'),

]
