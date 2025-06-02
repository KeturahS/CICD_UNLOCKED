from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from App_SetUp.models import StudentProfile
from GitExercises.models import Terminal_Exercises_Git_Commands, StudentGitCommandProgress
import pandas as pd
import io
import uuid

User = get_user_model()

class MonitorStudentGitProgressTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.lecturer_username = f"lecturer_{uuid.uuid4().hex[:6]}"
        self.student_username = f"student_{uuid.uuid4().hex[:6]}"
        self.cmd1_text = f"git init {uuid.uuid4().hex[:6]}"
        self.cmd2_text = f"git status {uuid.uuid4().hex[:6]}"

        # יצירת מרצה עם הרשאות מתאימות
        self.lecturer_user = User.objects.create_user(username=self.lecturer_username, password='test123')
        self.lecturer_user.is_staff = True
        self.lecturer_user.is_lecturer = True  # ✅ אם המערכת משתמשת בזה
        self.lecturer_user.save()

        # יצירת סטודנט
        self.student_user, _ = User.objects.get_or_create(username=self.student_username,
                                                          defaults={'password': 'test123'})
        self.student_profile, _ = StudentProfile.objects.get_or_create(user=self.student_user)

        self.cmd1 = Terminal_Exercises_Git_Commands.objects.create(command=self.cmd1_text)
        self.cmd2 = Terminal_Exercises_Git_Commands.objects.create(command=self.cmd2_text)

        StudentGitCommandProgress.objects.update_or_create(
            student=self.student_profile, command=self.cmd1,
            defaults={'completed': True, 'attempts': 1}
        )
        StudentGitCommandProgress.objects.update_or_create(
            student=self.student_profile, command=self.cmd2,
            defaults={'completed': False, 'attempts': 3}
        )

        # התחברות כמרצה
        logged_in = self.client.login(username=self.lecturer_username, password='test123')
        self.assertTrue(logged_in)

    def test_monitor_view_status_code(self):
        response = self.client.get(reverse('monitor_student_git_progress'))
        self.assertEqual(response.status_code, 200)

    def test_monitor_context_data(self):
        response = self.client.get(reverse('monitor_student_git_progress'))
        self.assertIsNotNone(response.context)
        self.assertIn('student_list', response.context)
        self.assertIn('summary', response.context)
        self.assertIn('bar_graph', response.context)
        self.assertIn('pie_chart', response.context)

    def test_monitor_summary_filter_best(self):
        response = self.client.get(reverse('monitor_student_git_progress') + '?table_filter=best')
        self.assertEqual(response.status_code, 200)
        summary = response.context['summary']
        for row in summary:
            self.assertLessEqual(row['avg_attempts'], 2.5)

    def test_monitor_summary_filter_struggle(self):
        response = self.client.get(reverse('monitor_student_git_progress') + '?table_filter=struggle')
        self.assertEqual(response.status_code, 200)
        summary = response.context['summary']
        for row in summary:
            self.assertGreaterEqual(row['avg_attempts'], 2.5)


class DownloadStudentReportTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.lecturer_username = f"lecturer_{uuid.uuid4().hex[:6]}"
        self.student_username = f"student_{uuid.uuid4().hex[:6]}"
        self.cmd1_text = f"git clone {uuid.uuid4().hex[:6]}"
        self.cmd2_text = f"git push {uuid.uuid4().hex[:6]}"

        self.lecturer_user = User.objects.create_user(username=self.lecturer_username, password='test123')
        self.lecturer_user.is_staff = True
        self.lecturer_user.is_lecturer = True  # ✅ כנ"ל
        self.lecturer_user.save()

        self.student_user, _ = User.objects.get_or_create(username=self.student_username,
                                                          defaults={'password': 'test123'})
        self.student_profile, _ = StudentProfile.objects.get_or_create(user=self.student_user)

        self.cmd1 = Terminal_Exercises_Git_Commands.objects.create(command=self.cmd1_text)
        self.cmd2 = Terminal_Exercises_Git_Commands.objects.create(command=self.cmd2_text)

        StudentGitCommandProgress.objects.update_or_create(
            student=self.student_profile, command=self.cmd1,
            defaults={'completed': True, 'attempts': 2}
        )
        StudentGitCommandProgress.objects.update_or_create(
            student=self.student_profile, command=self.cmd2,
            defaults={'completed': True, 'attempts': 3}
        )

        logged_in = self.client.login(username=self.lecturer_username, password='test123')
        self.assertTrue(logged_in)

    def test_download_report_csv_content(self):
        response = self.client.post(reverse('download_student_report'), {'filter': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('student_git_progress_report.csv', response['Content-Disposition'])

        content = response.content.decode('utf-8')
        self.assertIn('student__user__username', content)
        self.assertIn('total_attempts', content)

    def test_download_report_best_filter(self):
        response = self.client.post(reverse('download_student_report'), {'filter': 'best'})
        self.assertEqual(response.status_code, 200)
        df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
        for _, row in df.iterrows():
            self.assertLessEqual(row['avg_attempts'], 2.5)

    def test_download_report_struggle_filter(self):
        progress = StudentGitCommandProgress.objects.filter(student=self.student_profile).first()
        progress.attempts = 10
        progress.save()

        response = self.client.post(reverse('download_student_report'), {'filter': 'struggle'})
        self.assertEqual(response.status_code, 200)
        df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
        for _, row in df.iterrows():
            self.assertGreater(row['avg_attempts'], 2.5)
