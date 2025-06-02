from django.test import TestCase, Client
from django.urls import reverse
from App_SetUp.models import User, LecturerToAdminMessage
from django.test import TestCase, Client

class LecturerToAdminMessageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.lecturer = User.objects.create_user(
            username='lectest',
            password='lect1234',
            is_lecturer=True
        )
        self.url = reverse('send_message_to_admin')

    def test_lecturer_can_access_message_form(self):
        """בדיקה שהמרצה יכול לגשת לטופס שליחת הודעה לאדמין"""
        self.client.login(username='lectest', password='lect1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'שליחת הודעה לאדמין')

    def test_lecturer_can_send_message(self):
        """בדיקה שהמרצה שולח הודעה וההודעה נשמרת"""
        self.client.login(username='lectest', password='lect1234')
        response = self.client.post(self.url, {'content': 'זוהי הודעת בדיקה'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(LecturerToAdminMessage.objects.filter(sender=self.lecturer, content='זוהי הודעת בדיקה').exists())

    def test_anonymous_user_redirected_to_login(self):
        """בדיקה שמשתמש לא מחובר לא יכול לגשת"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_only_lecturer_can_access(self):
        """בדיקה שרק מרצה יכול לגשת – סטודנט או אדמין לא"""
        student = User.objects.create_user(username='student', password='student123', is_student=True)
        self.client.login(username='student', password='student123')
        response = self.client.get(self.url)
        # הוא אמור לקבל הפניה/חסימה
        self.assertNotEqual(response.status_code, 200)


class LecturerToAdminMessageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.lecturer = User.objects.create_user(username='lectest', password='lect1234', is_lecturer=True)
        self.student = User.objects.create_user(username='student', password='student123', is_student=True)
        self.admin = User.objects.create_user(username='admin', password='admin123', is_admin=True, is_staff=True)
        self.url = reverse('send_message_to_admin')

    def test_lecturer_can_access_message_form(self):
        """מרצה יכול לגשת לטופס ההודעה"""
        self.client.login(username='lectest', password='lect1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'שליחת הודעה לאדמין')

    def test_lecturer_can_send_message(self):
        """מרצה שולח הודעה וההודעה נשמרת במסד"""
        self.client.login(username='lectest', password='lect1234')
        response = self.client.post(self.url, {'content': 'זוהי הודעת בדיקה'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(LecturerToAdminMessage.objects.filter(sender=self.lecturer, content='זוהי הודעת בדיקה').exists())

    def test_anonymous_user_redirected_to_login(self):
        """משתמש לא מחובר לא יכול לגשת"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_only_lecturer_can_access(self):
        """סטודנט לא יכול לגשת"""
        self.client.login(username='student', password='student123')
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_message_with_empty_content_not_saved(self):
        """לא שומרים הודעה ריקה"""
        self.client.login(username='lectest', password='lect1234')
        response = self.client.post(self.url, {'content': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'תוכן ההודעה')  # כלומר: חזרנו לטופס עם שגיאה

    def test_post_form_invalid_data(self):
        """שולחים שדה לא קיים – לא אמור להישמר"""
        self.client.login(username='lectest', password='lect1234')
        response = self.client.post(self.url, {'fake_field': 'משהו'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(LecturerToAdminMessage.objects.exists())

    def test_multiple_messages_saved_separately(self):
        """בדיקה ששתי הודעות נשמרות בנפרד"""
        self.client.login(username='lectest', password='lect1234')
        self.client.post(self.url, {'content': 'הודעה ראשונה'})
        self.client.post(self.url, {'content': 'הודעה שנייה'})
        self.assertEqual(LecturerToAdminMessage.objects.filter(sender=self.lecturer).count(), 2)

    def test_admin_cannot_send_as_lecturer(self):
        """אדמין לא אמור לגשת לטופס של המרצה"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_correct_template_used(self):
        """בודק שהתבנית הנכונה נטענת"""
        self.client.login(username='lectest', password='lect1234')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'messages/send_message_to_admin.html')