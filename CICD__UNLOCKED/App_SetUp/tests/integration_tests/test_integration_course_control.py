from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from App_SetUp.models import CourseContent
import uuid

User = get_user_model()

class IntegrationTestCourseContentVisibility(TestCase):
    def setUp(self):
        self.client = Client()

        # יצירת משתמשים ייחודיים
        self.lecturer_username = f"lecturer_{uuid.uuid4().hex[:6]}"
        self.student_username = f"student_{uuid.uuid4().hex[:6]}"

        # מרצה
        self.lecturer = User.objects.create_user(
            username=self.lecturer_username,
            password='pass123',
            is_lecturer=True
        )

        # סטודנט
        self.student = User.objects.create_user(
            username=self.student_username,
            password='pass123',
            is_student=True
        )

        # יצירת מודולים עם מצבי נראות שונים
        self.module_git = CourseContent.objects.create(
            module='git',
            title='מודול Git',
            description='תיאור Git',
            visibility_mode='immediate',
            owner=self.lecturer
        )

        self.module_jenkins = CourseContent.objects.create(
            module='jenkins',
            title='מודול Jenkins',
            description='תיאור Jenkins',
            visibility_mode='hidden',
            owner=self.lecturer
        )

        self.module_docker = CourseContent.objects.create(
            module='docker',
            title='מודול Docker',
            description='תיאור Docker',
            visibility_mode='immediate',
            owner=self.lecturer
        )






class IntegrationTestCourseContentUpdate(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = 'pass123'

        self.lecturer_username = f"lecturer_{uuid.uuid4().hex[:6]}"
        self.lecturer = User.objects.create_user(
            username=self.lecturer_username,
            password=self.password,
            is_lecturer=True
        )

        self.git_content = CourseContent.objects.create(
            module='git',
            title='מודול Git',
            description='מודול בדיקה',
            visibility_mode='hidden',  # מתחיל מוסתר
            owner=self.lecturer
        )

    def test_lecturer_can_update_visibility_mode(self):
        # 🔐 התחברות כמרצה
        self.assertTrue(self.client.login(username=self.lecturer_username, password=self.password))

        # שליחת טופס עדכון (נניח שיש לך view בשם change_visibility_mode שמטפל בזה)
        response = self.client.post(
            reverse('update_module_visibility', args=[self.git_content.pk]),
            {'visibility_mode': 'immediate'}
        )

        self.assertEqual(response.status_code, 302)  # צפוי רידיירקט

        # רענון מהמסד
        self.git_content.refresh_from_db()
        self.assertEqual(self.git_content.visibility_mode, 'immediate')

        # ✅ בדיקת הופעה של המודול בדף הבית של סטודנט
        # ניצור סטודנט
        student = User.objects.create_user(
            username=f"student_{uuid.uuid4().hex[:6]}",
            password='pass123',
            is_student=True
        )
        self.client.logout()
        self.client.login(username=student.username, password='pass123')

        response = self.client.get(reverse('learning_home'))
        self.assertEqual(response.status_code, 200)
        visible_modules = response.context['visible_modules']
        self.assertIn('git', visible_modules)
