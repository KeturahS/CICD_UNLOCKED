import pytest
from django.test import TestCase, Client
from django.urls import reverse
from App_SetUp.models import User, StudentProfile
from GitExercises.models import Terminal_Exercises_Git_Commands, StudentGitCommandProgress

@pytest.mark.django_db
class TestGitExerciseVisibility(TestCase):
    """
    בדיקת אינטגרציה IT-02:
    יצירת 3 תרגילי Git ע״י מרצה, שיוכו לסטודנט, ואימות הופעתם בעמוד המודול של הסטודנט.
    """


    def setUp(self):
        # יצירת לקוח לבדיקה (client = סימולציה של דפדפן)
        self.client = Client()

        # יצירת משתמש מרצה
        self.lecturer = User.objects.create_user(username='lecturer1', password='pass123')
        self.lecturer.is_staff = True
        self.lecturer.save()

        # יצירת סטודנט
        self.student_user = User.objects.create_user(username='student1', password='pass123')
        self.student_profile = StudentProfile.objects.create(user=self.student_user)

        # יצירת תרגילי Git ושיוכם לסטודנט
        for i in range(6):
            git_command, _ = Terminal_Exercises_Git_Commands.objects.get_or_create(
                command=f'git command {i}',
                git_command_scenario=f'scenario {i}',
                level='basic'
            )
            StudentGitCommandProgress.objects.get_or_create(
                student=self.student_profile,
                command=git_command,
                completed=False
            )

    def test_git_exercises_visible_to_student_after_creation(self):
        # התחברות כסטודנט
        login_successful = self.client.login(username='student1', password='pass123')
        self.assertTrue(login_successful, "ההתחברות כסטודנט נכשלה")

        # גישה לעמוד התרגילים
        response = self.client.get(reverse('GitScenarioExercise'))

        # ווידוא שהעמוד נטען בהצלחה
        self.assertEqual(response.status_code, 200)

        # בדיקה שכל תרחישי ה-Git מופיעים בדף
        for i in range(6):
            self.assertContains(response, f'scenario {i}')
