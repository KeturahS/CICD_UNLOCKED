from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from App_SetUp.models import StudentProfile

User = get_user_model()

class StudentProfileViewTest(TestCase):
    def setUp(self):
        # יצירת משתמש חדש עם כל הפרטים הנדרשים
        self.student_user = User.objects.create_user(
            username='student123',
            password='testpass',
            first_name='f1',
            last_name='l1',
            email='student@example.com',
            is_student=True
        )

        # get_or_create כדי למנוע שגיאה של כפילות, ואז נעדכן את הפרטים הרצויים
        self.student_profile, _ = StudentProfile.objects.get_or_create(user=self.student_user)
        self.student_profile.institution = 'SCE'
        self.student_profile.target_completion_date = '2026-07-01'
        self.student_profile.save()

    def test_view_student_profile_authenticated(self):
        # התחברות עם המשתמש
        self.client.login(username='student123', password='testpass')

        # שליפת עמוד הפרופיל
        response = self.client.get(reverse('student_profile'))

        # בדיקות שהדף נטען והפרטים מוצגים
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'f1')              # שם פרטי
        self.assertContains(response, 'l1')            # שם משפחה
        self.assertContains(response, 'student@example.com')  # אימייל
        self.assertContains(response, 'SCE')               # מוסד לימודים
        self.assertContains(response, '2026')              # שנה מתאריך יעד

    def test_student_profile_requires_login(self):
        # בלי התחברות
        response = self.client.get(reverse('student_profile'))
        self.assertEqual(response.status_code, 302)  # אמור להפנות למסך התחברות
