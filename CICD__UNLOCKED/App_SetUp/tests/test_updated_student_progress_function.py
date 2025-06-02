from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date

from App_SetUp.models import (
    User, StudentProfile, StudentVideoCompletion, StudentPresentationCompletion,
    LearningVideo, Presentation
)
from GitExercises.models import (StudentGitCommandProgress, StudentJenkinsQuizExercise, Terminal_Exercises_Git_Commands,
    JenkinsConceptsQuiz)


class StudentProgressViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='student1', password='testpass123')
        self.student_profile = StudentProfile.objects.create(user=self.user, target_completion_date=date.today())

    def test_student_progress_view_returns_200(self):
        self.client.login(username='student1', password='testpass123')
        response = self.client.get(reverse('student_progress'))  # ודא שזה שם ה-url
        self.assertEqual(response.status_code, 200)

    def test_student_progress_initial_values(self):
        self.client.login(username='student1', password='testpass123')
        response = self.client.get(reverse('student_progress'))

        # Context data
        context = response.context

        self.assertEqual(context['git_progress'], 0)
        self.assertEqual(context['jenkins_progress'], 0)
        self.assertEqual(context['git_total'], 0)
        self.assertEqual(context['jenkins_total'], 0)
        self.assertEqual(context['git_completed'], 0)
        self.assertEqual(context['jenkins_completed'], 0)

    def test_git_progress_single_uncompleted(self):
        git_command_obj, _ = Terminal_Exercises_Git_Commands.objects.get_or_create(
            command='git commit',
            level='basic'
        )

        StudentGitCommandProgress.objects.update_or_create(
            student=self.student_profile,
            command=git_command_obj,
            defaults={'completed': False}
        )

        self.client.login(username='student1', password='testpass123')
        response = self.client.get(reverse('student_progress'))
        context = response.context

        self.assertEqual(context['git_progress'], 0)
        self.assertEqual(context['git_total'], 1)
        self.assertEqual(context['git_completed'], 0)

    def test_git_progress_single_completed(self):
        git_command_obj, _ = Terminal_Exercises_Git_Commands.objects.get_or_create(
            command='git init',
            level='basic'
        )

        StudentGitCommandProgress.objects.update_or_create(
            student=self.student_profile,
            command=git_command_obj,
            defaults={'completed': True}
        )

        self.client.login(username='student1', password='testpass123')
        response = self.client.get(reverse('student_progress'))
        context = response.context

        self.assertEqual(context['git_progress'], 100)
        self.assertEqual(context['git_total'], 1)
        self.assertEqual(context['git_completed'], 1)

    def test_git_progress_mixed_completion(self):
        cmd1, _ = Terminal_Exercises_Git_Commands.objects.get_or_create(command='git status', level='basic')
        cmd2, _ = Terminal_Exercises_Git_Commands.objects.get_or_create(command='git push', level='basic')

        StudentGitCommandProgress.objects.update_or_create(
            student=self.student_profile,
            command=cmd1,
            defaults={'completed': True}
        )
        StudentGitCommandProgress.objects.update_or_create(
            student=self.student_profile,
            command=cmd2,
            defaults={'completed': False}
        )

        self.client.login(username='student1', password='testpass123')
        response = self.client.get(reverse('student_progress'))
        context = response.context

        self.assertEqual(context['git_total'], 2)
        self.assertEqual(context['git_completed'], 1)
        self.assertEqual(context['git_progress'], 50)
