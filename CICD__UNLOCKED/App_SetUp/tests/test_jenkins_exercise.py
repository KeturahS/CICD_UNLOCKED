from django.test import TestCase, Client
from django.urls import reverse
from GitExercises.models import JenkinsConceptsQuiz, StudentJenkinsQuizExercise
from django.contrib.auth import get_user_model
from App_SetUp.models import StudentProfile
from django.urls import reverse

User = get_user_model()



class JenkinsSectionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('JenkinsSection')  # תוודא שהשם תואם ל-urls.py שלך
        self.quiz_question = JenkinsConceptsQuiz.objects.create(
            question='What is Jenkins?',
            option1='CI tool',
            option2='CD tool',
            option3='Testing tool',
            option4='Build tool',
            answer='CI tool'
        )

    def test_get_request_renders_correctly(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('JenkinsConceptsQuiz', response.context)
        self.assertIn('JenkinsConceptsQuizs_form', response.context)

    def test_post_add_question(self):
        data = {
            'add_question': '1',
            'question': 'What is a Jenkins pipeline?',
            'answer1': 'Automation script',
            'answer2': 'Manual process',
            'answer3': 'Deployment',
            'answer4': 'Test suite',
            'correct_answer': 'Automation script',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(JenkinsConceptsQuiz.objects.filter(question='What is a Jenkins pipeline?').exists())

    def test_post_update_question(self):
        data = {
            'update_question': '1',
            'question_id': self.quiz_question.id,
            'question': 'Updated question text',
            'answer1': 'Option A',
            'answer2': 'Option B',
            'answer3': 'Option C',
            'answer4': 'Option D',
            'correct_answer': 'Option A',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.quiz_question.refresh_from_db()
        self.assertEqual(self.quiz_question.question, 'Updated question text')
        self.assertEqual(self.quiz_question.option1, 'Option A')
        self.assertEqual(self.quiz_question.answer, 'Option A')

    def test_post_delete_question(self):
        data = {
            'delete_question': '1',
            'question_id': self.quiz_question.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(JenkinsConceptsQuiz.objects.filter(id=self.quiz_question.id).exists())


from django.test import TestCase, Client

from App_SetUp.models import StudentProfile
from django.urls import reverse


class UpdateJenkinsQuizCompletionTest(TestCase):
    def setUp(self):
        # יצירת משתמש ופרופיל סטודנט
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.student_profile = StudentProfile.objects.create(user=self.user)

        # יצירת שאלה ותרגיל לסטודנט
        quiz = JenkinsConceptsQuiz.objects.create(
            question='Sample question',
            option1='A',
            option2='B',
            option3='C',
            option4='D',
            answer='A'
        )
        self.student_quiz_exercise = StudentJenkinsQuizExercise.objects.create(
            student=self.student_profile,
            quiz=quiz,
            completed=False,
            score=0,
            attempts=0
        )

        self.client = Client()
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('update_jenkins_quiz_completion')  # וודא ששם ה-URL נכון ב-urls.py

    def test_post_complete_quiz_updates_completed_true(self):
        response = self.client.post(self.url, {'complete_quiz': 'true'})
        self.assertEqual(response.status_code, 200)
        # טוענים מחדש את האובייקט מהDB כדי לוודא העדכון
        self.student_quiz_exercise.refresh_from_db()
        self.assertTrue(self.student_quiz_exercise.completed)

    def test_post_without_complete_quiz_param_does_not_update(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.student_quiz_exercise.refresh_from_db()
        self.assertFalse(self.student_quiz_exercise.completed)

    def test_get_request_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.student_quiz_exercise.refresh_from_db()
        self.assertFalse(self.student_quiz_exercise.completed)
