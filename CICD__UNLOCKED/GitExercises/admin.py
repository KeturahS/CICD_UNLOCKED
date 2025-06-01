from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import GitHubSentence, Terminal_Exercises_Git_Commands, StudentGitCommandProgress, JenkinsConceptsQuiz, \
    StudentJenkinsQuizExercise, StudentPipelineAttempt,PipelineTemplate
from .models import GitSentence

admin.site.register(GitHubSentence)
admin.site.register(GitSentence)
admin.site.register(Terminal_Exercises_Git_Commands)
admin.site.register(StudentGitCommandProgress)
admin.site.register(JenkinsConceptsQuiz)
admin.site.register(StudentJenkinsQuizExercise)
admin.site.register(PipelineTemplate)
admin.site.register(StudentPipelineAttempt)