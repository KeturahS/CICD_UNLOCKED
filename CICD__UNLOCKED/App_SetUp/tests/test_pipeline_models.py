from django.test import TestCase
from django.contrib.auth import get_user_model
from GitExercises.models import PipelineTemplate, StudentPipelineAttempt
import uuid

User = get_user_model()

class PipelineUnitTests(TestCase):
    def setUp(self):
        self.student_user = User.objects.create_user(
            username=f"student_{uuid.uuid4().hex[:6]}",
            password="pass123",
            is_student=True
        )
        self.pipeline = PipelineTemplate.objects.create(
            title="Unit Test Pipeline",
            description="Basic test",
            initial_code="""
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
        )

    def test_pipeline_creation(self):
        self.assertEqual(PipelineTemplate.objects.count(), 1)
        self.assertEqual(self.pipeline.title, "Unit Test Pipeline")

    def test_attempt_creation_and_fields(self):
        attempt = StudentPipelineAttempt.objects.create(
            student=self.student_user,
            pipeline=self.pipeline,
            attempts=2,
            is_solved=True
        )
        self.assertEqual(attempt.attempts, 2)
        self.assertTrue(attempt.is_solved)
