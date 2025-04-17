from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import mail

User = get_user_model()

class LecturerRequestTests(TestCase):
    def setUp(self):
        self.client = Client()
        # יצירת מנהל מערכת מחובר
        self.admin_user = User.objects.create_user(
            username='adminuser', email='admin@example.com', password='adminpass',
            is_superuser=True, is_admin=True, is_active=True
        )
        self.client.login(username='adminuser', password='adminpass')

        # יצירת משתמש שמבקש להיות מרצה
        self.pending_lecturer = User.objects.create_user(
            username='pendinglecturer', email='lecturer@example.com', password='pass123',
            is_active=False, is_lecturer=True
        )

    def test_approve_lecturer_request(self):
        response = self.client.post(reverse('handle_lecturer_request'), {
            'user_email': self.pending_lecturer.email,
            'action': 'approve'
        })

        self.pending_lecturer.refresh_from_db()
        self.assertTrue(self.pending_lecturer.is_active)

        # בדיקה שנשלח מייל
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('אושר על ידי מנהל המערכת', mail.outbox[0].subject)
        self.assertRedirects(response, reverse('admin'))

    def test_reject_lecturer_request(self):
        response = self.client.post(reverse('handle_lecturer_request'), {
            'user_email': self.pending_lecturer.email,
            'action': 'reject'
        })

        # המשתמש נמחק
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(email=self.pending_lecturer.email)

        # בדיקה שנשלח מייל
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('סורבה על ידי מנהל המערכת', mail.outbox[0].subject)
        self.assertRedirects(response, reverse('admin'))
