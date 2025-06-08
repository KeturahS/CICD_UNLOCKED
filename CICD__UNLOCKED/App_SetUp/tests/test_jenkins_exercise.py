from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from GitExercises.models import JenkinsConceptsQuiz, StudentJenkinsQuizExercise
from App_SetUp.models import StudentProfile

User = get_user_model()


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
        self.url = reverse('update_jenkins_quiz_completion')  # וודא שהשם תואם ל-urls.py

    def test_post_complete_quiz_updates_completed_true(self):
        # שולחים את מזהה השאלה בפרמטר שכתוב אותו הפונקציה מצפה אליו
        data = {'correct_question_ids': str(self.student_quiz_exercise.quiz.id)}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.student_quiz_exercise.refresh_from_db()
        self.assertTrue(self.student_quiz_exercise.completed)

    def test_post_without_correct_question_ids_param_does_not_update(self):
        # POST בלי פרמטר, צריך להישאר לא מסומן כ- completed
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.student_quiz_exercise.refresh_from_db()
        self.assertFalse(self.student_quiz_exercise.completed)

    def test_get_request_returns_200(self):
        # בדיקת GET מחזיר 200
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.student_quiz_exercise.refresh_from_db()
        self.assertFalse(self.student_quiz_exercise.completed)
