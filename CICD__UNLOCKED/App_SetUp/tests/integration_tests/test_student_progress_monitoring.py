from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from App_SetUp.models import StudentProfile
from GitExercises.models import Terminal_Exercises_Git_Commands, StudentGitCommandProgress
import uuid

User = get_user_model()

class IntegrationTestStudentProgress(TestCase):
    def setUp(self):
        self.client = Client()

        # 🔐 יצירת יוזרים ייחודיים
        self.student_username = f"student_{uuid.uuid4().hex[:6]}"
        self.lecturer_username = f"lecturer_{uuid.uuid4().hex[:6]}"
        self.command_text = f"git test-{uuid.uuid4().hex[:6]}"

        # יצירת משתמשים
        self.lecturer = User.objects.create_user(username=self.lecturer_username, password='pass123', is_lecturer=True)
        self.student_user = User.objects.create_user(username=self.student_username, password='pass123', is_student=True)
        self.student_profile = StudentProfile.objects.create(user=self.student_user)

        # יצירת פקודת Git ייחודית
        self.command = Terminal_Exercises_Git_Commands.objects.create(
            command=self.command_text,
            Hebrew_Command='פקודת בדיקה'
        )

    def test_full_student_progress_flow(self):
        # 🧪 התחברות כסטודנט
        self.assertTrue(self.client.login(username=self.student_username, password='pass123'))

        # 💡 ניסיון פתרון לפקודת Git
        progress, created = StudentGitCommandProgress.objects.update_or_create(
            student=self.student_profile,
            command=self.command,
            defaults={'completed': True, 'attempts': 1}
        )
        self.assertTrue(created or progress.attempts == 1)

        self.client.logout()

        # 🧪 התחברות כמרצה
        self.assertTrue(self.client.login(username=self.lecturer_username, password='pass123'))

        # 📊 בדיקת עמוד ניטור התקדמות
        response = self.client.get(reverse('monitor_student_git_progress'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ניטור התקדמות סטודנטים')
        self.assertTemplateUsed(response, 'LecturerPages/monitor_student_progress.html')

        context = response.context
        for key in ['summary', 'student_list', 'bar_graph', 'pie_chart']:
            self.assertIn(key, context)

        summary = context['summary']
        usernames = [s['student__user__username'] for s in summary]
        self.assertIn(self.student_username, usernames)

        student_data = next(s for s in summary if s['student__user__username'] == self.student_username)
        self.assertEqual(student_data['total_attempts'], 1)
        self.assertEqual(student_data['total_completed'], 1)
        self.assertAlmostEqual(student_data['avg_attempts'], 1.0, places=2)

        # ⭐ בדיקת סינון "מצטיינים"
        response_best = self.client.get(reverse('monitor_student_git_progress'), {'filter': 'best'})
        self.assertEqual(response_best.status_code, 200)
        best_summary = response_best.context['summary']
        best_usernames = [s['student__user__username'] for s in best_summary]
        self.assertIn(self.student_username, best_usernames)

        # 📄 בדיקת הורדת CSV
        response_csv = self.client.post(reverse('download_student_report'), {'filter': 'best'})
        self.assertEqual(response_csv.status_code, 200)
        self.assertEqual(response_csv['Content-Type'], 'text/csv')
        self.assertIn(self.student_username, response_csv.content.decode('utf-8'))
