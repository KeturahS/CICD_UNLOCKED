from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from App_SetUp.models import User, ContactMessage


class RequestHandlingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(username='admin', email='admin@test.com', password='adminpass',
                                              is_admin=True, is_active=True, is_superuser=True)
        self.lecturer = User.objects.create_user(username='lecturer1', email='lect@test.com', password='lectpass',
                                                 is_lecturer=True, is_active=False)
        self.student = User.objects.create_user(username='student1', email='student@test.com', password='studentpass',
                                                is_student=True, is_active=True)

        self.admin.login = self.client.login(username='admin', password='adminpass')
        self.contact_message = ContactMessage.objects.create(
            student=self.student,
            category='admin',
            subject='בדיקת מערכת',
            message='האם ניתן לטפל בבאג?',
        )

    def test_approve_lecturer_request(self):
        response = self.client.post(reverse('handle_lecturer_request'), {
            'user_email': self.lecturer.email,
            'action': 'approve'
        })
        self.lecturer.refresh_from_db()
        self.assertTrue(self.lecturer.is_active)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("אושר", mail.outbox[0].subject)

    def test_reject_lecturer_request(self):
        response = self.client.post(reverse('handle_lecturer_request'), {
            'user_email': self.lecturer.email,
            'action': 'reject'
        })
        self.assertFalse(User.objects.filter(email=self.lecturer.email).exists())
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("סורבה", mail.outbox[0].subject)

    def test_resolve_admin_message(self):
        response = self.client.get(reverse('resolve_request', args=[self.contact_message.id]))
        self.contact_message.refresh_from_db()
        self.assertTrue(self.contact_message.is_resolved)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("טופלה", mail.outbox[0].subject)
