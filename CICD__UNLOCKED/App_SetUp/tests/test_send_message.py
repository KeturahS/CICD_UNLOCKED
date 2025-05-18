from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from App_SetUp.models import PrivateMessage
from App_SetUp.forms import PrivateMessageForm
from django.urls import reverse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


User = get_user_model()

class PrivateMessageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.lecturer = User.objects.create_user(username='lecturer', password='1234', is_lecturer=True)
        self.student = User.objects.create_user(username='student', password='1234', is_student=True)

    def test_send_private_message(self):
        self.client.login(username='lecturer', password='1234')

        data = {
            'recipient': self.student.id,
            'subject': 'בדיקת מערכת',
            'message': 'שלום לך סטודנט יקר!'
        }

        response = self.client.post('/lecturer/send-message/', data)

        # בדיקה שההודעה נשלחה והועברנו לעמוד הצלחה (200)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(PrivateMessage.objects.count(), 1)

        msg = PrivateMessage.objects.first()
        self.assertEqual(msg.sender, self.lecturer)
        self.assertEqual(msg.recipient, self.student)
        self.assertEqual(msg.subject, 'בדיקת מערכת')
        self.assertEqual(msg.message, 'שלום לך סטודנט יקר!')
