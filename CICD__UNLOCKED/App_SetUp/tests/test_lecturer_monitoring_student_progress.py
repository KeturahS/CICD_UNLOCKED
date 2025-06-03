from django.test import TestCase, Client
from django.urls import reverse

from datetime import date



from App_SetUp.models import (
    StudentProfile, StudentVideoCompletion, StudentPresentationCompletion,
    StudentGeneralProgress, LearningVideo, Presentation
)
from GitExercises.models import StudentGitCommandProgress, StudentJenkinsQuizExercise, Terminal_Exercises_Git_Commands, \
    JenkinsConceptsQuiz
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model



User = get_user_model()

class MonitorUpdatedStudentProgressTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.lecturer_user = User.objects.create_user(username='lecturer', password='lecturerpass')
        self.lecturer_user.is_staff = True
        self.lecturer_user.save()

        self.student_user = User.objects.create_user(username='student1', password='pass123')
        self.student = StudentProfile.objects.create(user=self.student_user, target_completion_date=date.today())

        self.url = reverse('monitor_updated_student_progress')  # ודא שזה תואם ל-urlname שלך

    def test_view_requires_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # צריך להפנות ל-login

    def test_view_returns_200_for_logged_in_user(self):
        self.client.login(username='lecturer', password='lecturerpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_progress_created_and_calculated_correctly(self):
        self.client.login(username='lecturer', password='lecturerpass')

        # יצירת פקודות Git מדומות
        git_command_1, _ = Terminal_Exercises_Git_Commands.objects.get_or_create(
            command='git init',
            Hebrew_Command='git init',
            English_Description='Initialize a new Git repository.',
            Hebrew_Description='אתחול מאגר גיט חדש.',
            git_feedback='Initialized empty Git repository.',
            git_command_scenario='Start version control in an empty folder.',
            level='basic'
        )
        git_command_2,_ = Terminal_Exercises_Git_Commands.objects.get_or_create(
            command='git add .',
            Hebrew_Command='git add .',
            English_Description='Add all files to staging area.',
            Hebrew_Description='הוספת כל הקבצים לאזור ההמתנה.',
            git_feedback='Files added to staging area.',
            git_command_scenario='Prepare changes for commit.',
            level='basic'
        )

        # יצירת התקדמות Git
        StudentGitCommandProgress.objects.update_or_create(
            student=self.student,
            command=git_command_1,
            defaults={'completed': True}
        )

        StudentGitCommandProgress.objects.update_or_create(
            student=self.student,
            command=git_command_2,
            defaults={'completed': False}
        )

        # Jenkins
        quiz = JenkinsConceptsQuiz.objects.create(
            question="What is Jenkins?",
            option1="CI tool",
            option2="CDN",
            option3="Database",
            option4="Web server",
            answer="CI tool"
        )

        student_quiz_exercise = StudentJenkinsQuizExercise.objects.create(student=self.student, quiz=quiz,
                                                                          completed=False)

        # לפני העדכון: בדיקה שסטטוס ה-completed הוא False
        self.assertFalse(student_quiz_exercise.completed)
        # וידאו Git
        vid_git, created = LearningVideo.objects.get_or_create(title='Intro to Git', module='Git')
        StudentVideoCompletion.objects.get_or_create(student=self.student, video=vid_git, completed=True)

        # וידאו Jenkins
        vid_jenkins , created= LearningVideo.objects.get_or_create(title='Intro to Jenkins', module='Jenkins')
        StudentVideoCompletion.objects.get_or_create(student=self.student, video=vid_jenkins, completed=False)

        # מצגת Docker
        pres_docker , created = Presentation.objects.get_or_create(title='Docker Basics', module='Docker')
        StudentPresentationCompletion.objects.get_or_create(student=self.student, presentation=pres_docker, completed=True)

        # קריאה לפונקציית התצוגה
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # בדיקה שרשומת ההתקדמות נוצרה ונכונה
        prog = StudentGeneralProgress.objects.get(student=self.student)

        self.assertEqual(prog.git_progress, 50)  # Git commands 1 מתוך 2

        self.assertEqual(prog.git_vids_total, 1)
        self.assertEqual(prog.git_vids_completed, 1)
        self.assertEqual(prog.jenkins_vids_total, 1)
        self.assertEqual(prog.jenkins_vids_completed, 0)
        self.assertEqual(prog.docker_presentations_completed, 1)
        self.assertEqual(prog.docker_presentations_total, 1)

        # החישוב לפי כלל הפריטים (וידאו + מצגות)
        # Git: יש 1 וידאו סה"כ, הושלם 1, מצגות אין (0)
        # לכן git_general_progress = (1+0) / (1+0) * 100 = 100
        self.assertEqual(prog.git_general_progress, 100)

        # Jenkins: יש 1 וידאו, לא הושלם, מצגות אין, אז 0%
        self.assertEqual(prog.jenkins_general_progress, 0)

        # Docker: יש מצגת אחת שהושלמה, אין וידאו
        # docker_general_progress = (0+1) / (0+1) * 100 = 100
        self.assertEqual(prog.docker_general_progress, 100)

        self.assertEqual(prog.name, self.student_user.get_full_name())
        self.assertEqual(prog.email, self.student_user.email)
        self.assertEqual(prog.username, self.student_user.username)
