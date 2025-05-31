from django.db import models

from django.db import models
from django.utils import timezone
from App_SetUp.models import StudentProfile


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


class StudentGitHubGitAssignment(models.Model):
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name='github_git_assignment')
    completed = models.BooleanField(default=False)
    last_attempt = models.DateTimeField(auto_now=True)
    attempts = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student.user.username} - {'הושלם' if self.completed else 'לא הושלם'}"


class Terminal_Exercises_Git_Commands(models.Model):
    command = models.CharField(max_length=255)
    Hebrew_Command = models.CharField(max_length=255, default="")
    English_Description = models.TextField(default="")
    Hebrew_Description = models.TextField(default="")
    git_feedback = models.TextField(default="")
    git_command_scenario = models.TextField(default="")
    LEVELS = {
        'basic': 'basic',
        'branches': 'branches',
        'advanced': 'advanced',
    }
    level = models.CharField(max_length=20, choices=LEVELS.items(), default='beginner')
    def __str__(self):
        return self.command


class StudentGitCommandProgress(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='git_commands')
    command = models.ForeignKey(Terminal_Exercises_Git_Commands, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    last_attempt = models.DateTimeField(auto_now=True)
    attempts = models.IntegerField(default=0)

    class Meta:
        unique_together = ('student', 'command')

    def __str__(self):
        return f"{self.student.user.username} - {self.command.command}"

from django.db import models
from App_SetUp.models import StudentProfile
from django.contrib.postgres.fields import JSONField  # Use this for PostgreSQL

class JenkinsConceptsQuiz(models.Model):
    question = models.CharField(max_length=255)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question


class StudentJenkinsQuizExercise(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='jenkins_quizzes')
    quiz = models.ForeignKey(JenkinsConceptsQuiz, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'quiz'], name='unique_student_quiz')
        ]

    def __str__(self):
        return f"{self.student.user.username} - {self.quiz.question}"


