from django.test import TestCase, Client
from django.urls import reverse
from App_SetUp.models import User, StudentProfile
from GitExercises.models import PipelineTemplate, StudentPipelineAttempt

class PipelineIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()

        # יצירת משתמש סטודנט
        self.student, _ = User.objects.get_or_create(
            username='student1',
            defaults={
                'password': 'pass123',
                'is_student': True
            }
        )
        self.student.set_password('pass123')  # חשוב לשים סיסמה עם set_password
        self.student.save()

        # יצירת פרופיל סטודנט
        StudentProfile.objects.get_or_create(user=self.student, defaults={'institution': 'SCE'})

        # יצירת PipelineTemplate עם default קוד
        self.pipeline, _ = PipelineTemplate.objects.get_or_create(
            title="Test Pipeline",
            description="desc",
            defaults={
                "initial_code": """
                pipeline {
                    agent any
                    stages {
                        stage('Build') {
                            steps {
                                echo 'Building...'
                            }
                        }
                        stage('Test') {
                            steps {
                                echo 'Testing...'
                            }
                        }
                    }
                }
                """
            }
        )

        # התחברות
        self.client.login(username='student1', password='pass123')

    def test_pipeline_page_loads(self):
        """בודק שהעמוד הראשי של התרגול עולה תקין"""
        response = self.client.get(reverse('jenkins_questions'))
        self.assertEqual(response.status_code, 200)

    def test_pipeline_submission(self):
        """בודק ששליחת קוד נכון יוצרת ניסיון מוצלח ומתעדכנת"""
        response = self.client.post(
            reverse('handle_pipeline_submission'),
            {
                "pipeline_id": self.pipeline.id,
                "code": self.pipeline.initial_code
            }
        )
        self.assertEqual(response.status_code, 302)  # הפניה לעמוד התרגול

        # בדיקה שהניסיון נוצר כראוי
        attempt = StudentPipelineAttempt.objects.get(student=self.student, pipeline=self.pipeline)
        self.assertTrue(attempt.is_solved)
