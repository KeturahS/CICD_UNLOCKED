from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from App_SetUp.models import StudentProfile

User = get_user_model()

class UpdateStudentProfileTest(TestCase):
    def setUp(self):
        # יצירת סטודנט עם פרטי התחלה
        self.student_user = User.objects.create_user(
            username='student_update',
            password='testpass',
            first_name='ישן',
            last_name='ישןוביץ',
            email='old@example.com',
            is_student=True
        )

        # יצירת פרופיל סטודנט
        self.student_profile, _ = StudentProfile.objects.get_or_create(user=self.student_user)
        self.student_profile.institution = 'Old University'
        self.student_profile.target_completion_date = '2025-01-01'
        self.student_profile.save()

    def test_update_student_profile_valid_data(self):
        self.client.login(username='student_update', password='testpass')

        response = self.client.post(reverse('update_student_profile'), {
            'first_name': 'אילן',
            'last_name': 'אמוייב',
            'email': 'ilan@example.com',
            'institution': 'SCE',
            'target_completion_date': '2026-07-01'
        })

        # ודא שהטופס שולח redirect לאחר הצלחה
        self.assertRedirects(response, reverse('student_profile'))

        # טען מחדש את המשתמש והפרופיל
        self.student_user.refresh_from_db()
        self.student_profile.refresh_from_db()

        # בדוק שהתוכן עודכן
        self.assertEqual(self.student_user.first_name, 'אילן')
        self.assertEqual(self.student_user.last_name, 'אמוייב')
        self.assertEqual(self.student_user.email, 'ilan@example.com')
        self.assertEqual(self.student_profile.institution, 'SCE')
        self.assertEqual(str(self.student_profile.target_completion_date), '2026-07-01')

    def test_update_student_profile_requires_login(self):
        response = self.client.get(reverse('update_student_profile'))
        self.assertEqual(response.status_code, 302)  # redirect למסך התחברות
