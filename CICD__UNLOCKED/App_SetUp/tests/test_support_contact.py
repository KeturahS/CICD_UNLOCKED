from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from App_SetUp.models import ContactMessage

User = get_user_model()

class ContactSupportTest(TestCase):
    def setUp(self):
        self.student_user = User.objects.create_user(
            username='student_support',
            password='testpass',
            is_student=True
        )

    def test_send_valid_contact_message(self):
        self.client.login(username='student_support', password='testpass')

        response = self.client.post(reverse('contact_us'), {
            'category': 'support',
            'subject': 'בעיה במערכת',
            'message': 'אני לא מצליח להיכנס לחשבון שלי'
        })

        # בדוק האם התבצע redirect לאחר שליחה
        self.assertEqual(response.status_code, 302)

        # בדוק אם ההודעה באמת נשמרה במסד הנתונים
        self.assertEqual(ContactMessage.objects.count(), 1)
        msg = ContactMessage.objects.first()
        self.assertEqual(msg.student, self.student_user)
        self.assertEqual(msg.subject, 'בעיה במערכת')
        self.assertEqual(msg.category, 'support')
        self.assertEqual(msg.is_resolved, False)

    def test_contact_message_requires_login(self):
        response = self.client.get(reverse('contact_us'))
        self.assertEqual(response.status_code, 302)  # אמור להפנות למסך התחברות

    def test_invalid_contact_message_missing_fields(self):
        self.client.login(username='student_support', password='testpass')

        # שליחת טופס ריק
        response = self.client.post(reverse('contact_us'), {
            'category': '',
            'subject': '',
            'message': ''
        })

        # הטופס לא אמור להתקבל, ולכן לא יהיה redirect
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required', status_code=200)
        self.assertEqual(ContactMessage.objects.count(), 0)
