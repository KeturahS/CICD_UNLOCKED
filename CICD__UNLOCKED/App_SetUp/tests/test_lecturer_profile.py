from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from App_SetUp.models import LecturerProfile

User = get_user_model()

class LecturerProfileViewTest(TestCase):
    def setUp(self):
        # יצירת משתמש מרצה
        self.lecturer_user = User.objects.create_user(
            username='lecturer123',
            password='testpass',
            first_name='דנה',
            last_name='כהן',
            email='dana@example.com',
            is_lecturer=True
        )

        # יצירת LecturerProfile
        LecturerProfile.objects.create(user=self.lecturer_user)

    def test_view_lecturer_profile_authenticated(self):
        # התחברות
        self.client.login(username='lecturer123', password='testpass')

        # שליפת עמוד הפרופיל
        response = self.client.get(reverse('lecturer_profile'))

        # בדיקות שהעמוד נטען והתוכן מוצג
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'דנה')               # שם פרטי
        self.assertContains(response, 'כהן')               # שם משפחה
        self.assertContains(response, 'dana@example.com')  # אימייל
        self.assertContains(response, 'lecturer123')       # שם משתמש

    def test_lecturer_profile_requires_login(self):
        # בדיקה של ניסיון ללא התחברות
        response = self.client.get(reverse('lecturer_profile'))
        self.assertEqual(response.status_code, 302)
