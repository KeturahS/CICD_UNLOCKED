from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from App_SetUp.models import ContactMessage

User = get_user_model()

class ContactMessageFilterTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='adminuser',
            password='adminpass',
            is_admin=True,
            is_active=True
        )

        self.student_user = User.objects.create_user(
            username='studentuser',
            password='studentpass',
            is_student=True,
            is_active=True
        )

        # צור שתי פניות: אחת פתוחה ואחת סגורה
        self.open_message = ContactMessage.objects.create(
            student=self.student_user,
            category='support',
            subject='בעיה במערכת',
            message='המערכת לא עולה',
            is_resolved=False
        )
        self.closed_message = ContactMessage.objects.create(
            student=self.student_user,
            category='support',
            subject='בקשת שיפור',
            message='להוסיף פונקציה חדשה',
            is_resolved=True
        )

    def test_admin_view_all_messages(self):
        self.client.login(username='adminuser', password='adminpass')
        response = self.client.get(reverse('admin'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'בעיה במערכת')
        self.assertContains(response, 'בקשת שיפור')

    def test_admin_view_only_open_messages(self):
        self.client.login(username='adminuser', password='adminpass')
        response = self.client.get(reverse('admin') + '?show=open')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'בעיה במערכת')
        self.assertNotContains(response, 'בקשת שיפור')

