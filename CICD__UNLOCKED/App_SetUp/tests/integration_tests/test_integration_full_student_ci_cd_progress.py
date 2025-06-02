from django.test import TestCase, Client
from django.urls import reverse
from datetime import date
from django.contrib.auth import get_user_model  # <-- כאן

from App_SetUp.models import (
    StudentProfile, StudentVideoCompletion, StudentPresentationCompletion,
    LearningVideo, Presentation
)
from GitExercises.models import (
    StudentGitCommandProgress, StudentJenkinsQuizExercise, Terminal_Exercises_Git_Commands,
    JenkinsConceptsQuiz
)

User = get_user_model()  # <-- משתמשים בזה כדי לקבל את המודל המשתמש המותאם שלך

class StudentProgressViewIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='student1', password='testpass123')
        self.student_profile, created = StudentProfile.objects.get_or_create(user=self.user, target_completion_date=date.today())

    def test_full_student_ci_cd_journey(self):
        # שאר הקוד נשאר כפי שהוא
        ...

        # Create or get Git Command
        git_cmd, created = Terminal_Exercises_Git_Commands.objects.get_or_create(command='git push', level='advanced')

        # Create or get Jenkins Quiz
        jenkins_quiz, created = JenkinsConceptsQuiz.objects.get_or_create(
            question='What is a Jenkins Pipeline?',
            option1='A job scheduler',
            option2='A source control system',
            option3='A way to automate CI/CD',
            option4='An operating system',
            answer='A way to automate CI/CD'
        )

        # Create or get Learning Materials
        video, created = LearningVideo.objects.get_or_create(title='Intro to CI/CD', module='Git')
        presentation, created = Presentation.objects.get_or_create(title='CI/CD Overview', module='Git')

        # Mark progress using update_or_create to avoid UNIQUE constraint errors
        StudentGitCommandProgress.objects.update_or_create(
            student=self.student_profile,
            command=git_cmd,
            defaults={'completed': True}
        )
        StudentJenkinsQuizExercise.objects.update_or_create(
            student=self.student_profile,
            quiz=jenkins_quiz,
            defaults={'score': 90, 'completed': True}
        )
        StudentVideoCompletion.objects.update_or_create(
            student=self.student_profile,
            video=video,
            defaults={'completed': True}
        )
        StudentPresentationCompletion.objects.update_or_create(
            student=self.student_profile,
            presentation=presentation,
            defaults={'completed': True}
        )

        # Login and access progress page
        self.client.login(username='student1', password='testpass123')
        response = self.client.get(reverse('student_progress'))
        context = response.context

        # Assertions
        self.assertEqual(response.status_code, 200)

        # Git progress assertions
        self.assertEqual(context['git_total'], 1)
        self.assertEqual(context['git_completed'], 1)
        self.assertGreater(context['git_vids_completed'], 0)
        self.assertGreater(context['git_presentations_completed'], 0)

        # Jenkins progress assertions
        self.assertEqual(context['jenkins_total'], 1)
        self.assertEqual(context['jenkins_completed'], 1)

        # Learning content assertions
        self.assertGreater(len(StudentVideoCompletion.objects.filter(student=self.student_profile)), 0)
        self.assertGreater(len(StudentPresentationCompletion.objects.filter(student=self.student_profile)), 0)
