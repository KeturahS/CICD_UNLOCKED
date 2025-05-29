from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from unittest.mock import patch
from App_SetUp.models import ServerLoadRecord
from App_SetUp.utils.server_monitor import is_high_load, record_server_load
from App_SetUp.views import captcha_challenge
from django.test.client import RequestFactory, Client
from django.middleware.csrf import CsrfViewMiddleware

User = get_user_model()


class ServerLoadTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user.is_active = True
        self.user.is_student = True
        self.user.save()

    def test_record_server_load_creates_record(self):
        record_server_load()
        self.assertEqual(ServerLoadRecord.objects.count(), 1)

    def test_is_high_load_returns_false_when_empty(self):
        ServerLoadRecord.objects.all().delete()
        self.assertFalse(is_high_load())

    def test_is_high_load_true_for_high_cpu(self):
        ServerLoadRecord.objects.create(cpu_percent=90, memory_percent=60, disk_percent=40)
        self.assertTrue(is_high_load())

    def test_is_high_load_false_for_normal_load(self):
        ServerLoadRecord.objects.create(cpu_percent=40, memory_percent=50, disk_percent=30)
        self.assertFalse(is_high_load())


    @patch('App_SetUp.views.requests.post')
    def test_captcha_success_redirects(self, mock_post):
        # סימולציה של הצלחת אימות
        mock_post.return_value.json.return_value = {'success': True}

        session = self.client.session
        session['pending_username'] = self.user.username
        session['pending_password'] = 'testpass'
        session.save()

        response = self.client.post('/captcha/', {
            'g-recaptcha-response': 'valid_token',
        })

        self.assertEqual(response.status_code, 302)

    @patch('App_SetUp.views.requests.post')
    def test_captcha_failure_shows_error(self, mock_post):
        mock_post.return_value.json.return_value = {'success': False}

        response = self.client.post('/captcha/', {
            'g-recaptcha-response': 'invalid_token',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'האימות נכשל')

