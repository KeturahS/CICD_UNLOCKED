from django.db import models

# Create your models here.
class GitHubSentence(models.Model):
    sentence = models.CharField(max_length=255)
    type = "GitHub"
    def __str__(self):
        return self.sentence

class GitSentence(models.Model):
    sentence = models.CharField(max_length=255)
    type= "Git"
    def __str__(self):
        return self.sentence