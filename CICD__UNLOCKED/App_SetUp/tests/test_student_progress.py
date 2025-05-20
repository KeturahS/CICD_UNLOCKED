from django.contrib.auth import get_user_model

from App_SetUp.models import StudentProfile
from GitExercises.models import (
    Terminal_Exercises_Git_Commands,
    StudentGitCommandProgress,
    JenkinsConceptsQuiz,
    StudentJenkinsQuizExercise
)
from django.test import TestCase, Client
from django.urls import reverse
from datetime import date, timedelta
import uuid

User = get_user_model()

class GitAndJenkinsModelTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.student_username = f"student_{uuid.uuid4().hex[:6]}"
        self.command_text = f"git test-{uuid.uuid4().hex[:6]}"
        self.student_user = User.objects.create_user(
            username=self.student_username,
            password='pass123',
            is_student=True
        )
        self.student_profile = StudentProfile.objects.create(
            user=self.student_user,
            target_completion_date=date.today() + timedelta(days=10)
        )

        self.command = Terminal_Exercises_Git_Commands.objects.create(
            command=self.command_text,
            Hebrew_Command='פקודת בדיקה'
        )

        self.jenkins_question = JenkinsConceptsQuiz.objects.create(
            question='What is Jenkins used for?',
            option1='Continuous Integration',
            option2='Code Compilation',
            option3='Email Service',
            option4='Database Management',
            answer='Continuous Integration'
        )

    def test_git_command_progress_creation(self):
        self.assertTrue(self.client.login(username=self.student_username, password='pass123'))
        progress, created = StudentGitCommandProgress.objects.update_or_create(
            student=self.student_profile,
            command=self.command,
            defaults={'completed': True, 'attempts': 1}
        )
        self.assertTrue(created or progress.attempts == 1)

    def test_jenkins_quiz_submission(self):
        self.assertTrue(self.client.login(username=self.student_username, password='pass123'))
        progress, created = StudentJenkinsQuizExercise.objects.update_or_create(
            student=self.student_profile,
            quiz=self.jenkins_question,
            defaults={'completed': True, 'attempts': 1}
        )
        self.assertTrue(created or progress.attempts == 1)

    def test_student_progress_view(self):
        self.assertTrue(self.client.login(username=self.student_username, password='pass123'))
        StudentGitCommandProgress.objects.update_or_create(
            student=self.student_profile,
            command=self.command,
            defaults={'completed': True, 'attempts': 1}
        )

        StudentJenkinsQuizExercise.objects.update_or_create(
            student=self.student_profile,
            quiz=self.jenkins_question,
            defaults={'completed': True, 'attempts': 1}
        )

        response = self.client.get(reverse('student_progress'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('git_progress', response.context)
        self.assertIn('jenkins_progress', response.context)
        self.assertIn('days_remaining', response.context)
        self.assertEqual(response.context['git_progress'], 100)
        self.assertEqual(response.context['jenkins_progress'], 100)
        self.assertEqual(response.context['days_remaining'], 10)


