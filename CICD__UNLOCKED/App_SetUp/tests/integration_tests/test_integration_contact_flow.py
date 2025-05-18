from django.test import TestCase, Client
from django.urls import reverse
from App_SetUp.models import User, ContactMessage

class ContactIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = User.objects.create_user(username='student', password='pass', is_student=True, is_active=True)
        self.lecturer = User.objects.create_user(username='lecturer', password='pass', is_lecturer=True, is_active=True)

    def test_student_sends_message_and_lecturer_responds(self):
        # שלב 1 - התחברות כסטודנט
        self.client.login(username='student', password='pass')

        # שלב 2 - שליחת פנייה
        response = self.client.post(reverse('contact_us'), {
            'category': 'lecturer',
            'subject': 'שאלה על גיט',
            'message': 'איך משתמשים ב-commit?',
        })
        self.assertEqual(response.status_code, 302)  # מעבר לעמוד הצלחה

        contact = ContactMessage.objects.first()
        self.assertEqual(contact.student.username, 'student')
        self.assertFalse(contact.is_resolved)

        # שלב 3 - התחברות כמרצה
        self.client.logout()
        self.client.login(username='lecturer', password='pass')

        # שלב 4 - סימון הפנייה כ"נפתרה"
        response = self.client.get(reverse('resolve_lecturer_request', args=[contact.id]))
        self.assertEqual(response.status_code, 302)

        contact.refresh_from_db()
        self.assertTrue(contact.is_resolved)

        # שלב 5+6 - התחברות מחדש כסטודנט ובדיקה
        self.client.logout()
        self.client.login(username='student', password='pass')

        response = self.client.get(reverse('student_messages'))
        self.assertContains(response, 'טופלה')
