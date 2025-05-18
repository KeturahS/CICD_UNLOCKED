from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from App_SetUp.models import LearningModuleRating

User = get_user_model()

class RateModulesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = User.objects.create_user(
            username='student',
            password='1234',
            is_student=True
        )

    def test_rate_learning_modules(self):
        # התחברות כסטודנט
        self.client.login(username='student', password='1234')

        # שליחת POST עם דירוגים
        response = self.client.post('/student/rate_modules/', {
            'git_rating': '5',
            'git_comment': 'לומדה מצוינת!',
            'jenkins_rating': '4',
            'jenkins_comment': 'לא רע בכלל',
            'docker_rating': '3',
            'docker_comment': 'יכול להיות טוב יותר',
        })

        # בדיקה שהתגובה היא 200 והתקבלה הצלחה
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LearningModuleRating.objects.count(), 3)

        git_rating = LearningModuleRating.objects.get(module_name='Git')
        self.assertEqual(git_rating.rating, 5)
        self.assertEqual(git_rating.comment, 'לומדה מצוינת!')
        self.assertEqual(git_rating.student, self.student)
