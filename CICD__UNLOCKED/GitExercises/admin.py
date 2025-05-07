from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import GitHubSentence
from .models import GitSentence

admin.site.register(GitHubSentence)
admin.site.register(GitSentence)