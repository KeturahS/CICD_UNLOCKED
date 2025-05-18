from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import GitHubSentence, Terminal_Exercises_Git_Commands, StudentGitCommandProgress
from .models import GitSentence

admin.site.register(GitHubSentence)
admin.site.register(GitSentence)
admin.site.register(Terminal_Exercises_Git_Commands)
admin.site.register(StudentGitCommandProgress)