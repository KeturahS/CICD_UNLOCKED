from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from App_SetUp.models import LearningModuleRating

User = get_user_model()

class GitRatingIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='student1', password='testpass123', is_student=True)
        self.url = reverse('git_rating')  # ודא שזה השם שלך ב־urls.py

    def test_git_rating_submission(self):
        # התחברות כמשתמש סטודנט
        self.client.login(username='student1', password='testpass123')

        # שליחת דירוג דרך POST
        response = self.client.post(self.url, {
            'rating': '5',
            'comment': 'לומדה מעולה! עזרה לי להבין את Git'
        })

        # בדיקת הפניה לעמוד תודה (או תבנית אחרת)
        self.assertTemplateUsed(response, 'thank_you.html')

        # בדיקת שהדירוג נשמר במסד
        rating_entry = LearningModuleRating.objects.filter(student=self.user, module_name='Git').first()
        self.assertIsNotNone(rating_entry)
        self.assertEqual(rating_entry.rating, 5)
        self.assertEqual(rating_entry.comment, 'לומדה מעולה! עזרה לי להבין את Git')
