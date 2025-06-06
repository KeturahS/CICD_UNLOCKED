from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from App_SetUp.models import StudentProfile, LearningVideo, Presentation, StudentVideoCompletion

User = get_user_model()

class ModulesAndSectionsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.student_user = User.objects.create_user(username='student1', password='testpass')
        self.student_user.is_student = True
        self.student_user.is_active = True
        self.student_user.save()

        self.student_profile, _ = StudentProfile.objects.get_or_create(user=self.student_user, institution='SCE')

        # יצירת סרטונים למודולים Git ו-Jenkins
        self.videos = {}  # לשמירה על אובייקטי הסרטונים לפי module ו-step
        for module in ['Git', 'Jenkins']:
            for order in range(1, 4):
                video, _ = LearningVideo.objects.get_or_create(
                    title=f'{module} Video {order}',
                    youtube_id=f'{module.lower()}_{order}',
                    module=module,
                    order=order
                )
                self.videos[(module, order)] = video

                # יצירת סטטוס צפייה (כדי למנוע שגיאת .get())
                StudentVideoCompletion.objects.get_or_create(
                    student=self.student_profile,
                    video=video
                )

        # מצגות
        Presentation.objects.get_or_create(
            module='Docker',
            title='מצגת דוקר שלב 3',
            embed_url='https://slides.com/docker3',
            order=3
        )

        Presentation.objects.get_or_create(
            module='Jenkins',
            title='מצגת ג\'נקינס שלב 4',
            embed_url='https://slides.com/jenkins4',
            order=4
        )

    def login_and_get(self, url_name, params=None):
        self.client.login(username='student1', password='testpass')
        if params:
            return self.client.get(reverse(url_name) + params)
        return self.client.get(reverse(url_name))

    def test_git_module_page_loads(self):
        response = self.login_and_get('git_module', '?step=1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Git')

    def test_jenkins_module_page_loads(self):
        response = self.login_and_get('jenkins_module', '?step=2')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jenkins')

    def test_docker_module_page_loads(self):
        response = self.login_and_get('docker_module', '?step=3')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'iframe')

    def test_git_sections(self):
        for step in range(1, 4):
            response = self.login_and_get(f'git_section{step}')
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Git')

    def test_jenkins_sections(self):
        for step in range(1, 4):
            response = self.login_and_get(f'jenkins_section{step}')
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Jenkins')

        response = self.login_and_get('jenkins_section4')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'iframe')

    def test_docker_sections(self):
        for step in range(1, 3):
            response = self.login_and_get(f'docker_section{step}')
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Docker')

        response = self.login_and_get('docker_section3')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'iframe')
