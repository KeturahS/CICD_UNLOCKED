from django.test import TestCase, Client
from django.urls import reverse
from GitExercises.models import Terminal_Exercises_Git_Commands, StudentGitCommandProgress
from App_SetUp.models import User, StudentProfile
from datetime import date

class UpdateCommandStatusTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Create test user
        self.user = User.objects.create_user(
            username="studentuser1",
            email="student@example.com",
            password="testpassword",
            is_student=True
        )

        # Create student profile
        self.student_profile = StudentProfile.objects.create(
            user=self.user,
            institution="SCE",
            target_completion_date=date(2026, 6, 30)
        )

        # Create command
        self.command = Terminal_Exercises_Git_Commands.objects.create(
            command="git status",
            Hebrew_Command="סטטוס",
            English_Description="Show the working directory status",
            Hebrew_Description="מציג את מצב תיקיית העבודה",
            git_feedback="No changes",
            git_command_scenario="You made some changes and want to check the current status.",
            level="basic"
        )

        # Link command to student
        self.progress, created = StudentGitCommandProgress.objects.get_or_create(
            student=self.student_profile,
            command=self.command,
            defaults={'completed': False, 'attempts': 0}
        )

    def test_update_command_status_success(self):
        # Log in the test user
        self.client.login(username="studentuser1", password="testpassword")

        # Simulate POST request to the view
        response = self.client.post(reverse('update_command_status'), {
            'command': 'git status'
        }, follow=True)

        # Refresh from DB
        self.progress.refresh_from_db()

        # Assertions
        self.assertTrue(self.progress.completed)
        self.assertEqual(self.progress.attempts, 1)



from django.test import TestCase, Client
from django.urls import reverse
from App_SetUp.models import User, StudentProfile
from GitExercises.models import Terminal_Exercises_Git_Commands, StudentGitCommandProgress
from datetime import date

class UpdateCommandAttemptsStatusTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='studentuser1',
            email='student@example.com',
            password='testpassword',
            is_student=True
        )
        self.student_profile = StudentProfile.objects.create(
            user=self.user,
            institution='SCE',
            target_completion_date=date(2026, 6, 30)
        )

        self.command = Terminal_Exercises_Git_Commands.objects.create(
            command='git status',
            Hebrew_Command='סטטוס',
            English_Description='Show the working directory status',
            Hebrew_Description='מציג את מצב תיקיית העבודה',
            git_feedback='No changes',
            git_command_scenario='You made some changes and want to check the current status.',
            level='basic'
        )

        self.progress, created = StudentGitCommandProgress.objects.get_or_create(
            student=self.student_profile,
            command=self.command,
            defaults={'completed': False, 'attempts': 0}
        )

        self.client = Client()
        self.client.login(username='studentuser1', password='testpassword')

    def test_update_attempts_success(self):
        response = self.client.post(reverse('update_command_attempts_status'), data={'command': 'git status'})

        self.progress.refresh_from_db()
        self.assertEqual(self.progress.attempts, 1)
        self.assertRedirects(response, reverse('GitScenarioExercise'))



from django.test import TestCase, Client
from django.urls import reverse
from GitExercises.models import Terminal_Exercises_Git_Commands
from App_SetUp.models import User

class GitSection2ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a lecturer user (assuming only lecturers access this view)
        self.lecturer = User.objects.create_user(
            username='lecturer1',
            password='testpassword',
            is_lecturer=True
        )
        self.client.login(username='lecturer1', password='testpassword')

        # Create an initial Terminal Exercise
        self.exercise = Terminal_Exercises_Git_Commands.objects.create(
            command='git status',
            Hebrew_Command='סטטוס',
            English_Description='Show status',
            Hebrew_Description='הצג סטטוס',
            git_feedback='No changes',
            git_command_scenario='Check current status',
            level='basic'
        )

    def test_get_request_returns_context(self):
        response = self.client.get(reverse('GitSection2'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Terminal_Exercises', response.context)
        self.assertIn('Terminal_Exercises_form', response.context)
        self.assertIn('levels', response.context)
        self.assertIn(self.exercise, response.context['Terminal_Exercises'])

    def test_post_add_terminal_exercise_creates_new_exercise(self):
        post_data = {
            'add_terminal_exercise': 'true',
            'command': 'git add',
            'Hebrew_Command': 'הוסף',
            'description_en': 'Add files',
            'description_he': 'הוסף קבצים',
            'feedback': 'Added successfully',
            'scenario': 'Stage files',
            'level': 'intermediate',
        }
        response = self.client.post(reverse('GitSection2'), data=post_data)
        self.assertEqual(response.status_code, 200)  # renders page again
        self.assertTrue(Terminal_Exercises_Git_Commands.objects.filter(command='git add').exists())

    def test_post_update_terminal_exercise_updates_existing(self):
        post_data = {
            'update_terminal_exercise': 'true',
            'exercise_id': str(self.exercise.id),
            'command': 'git status updated',
            'description_en': 'Updated description',
            'description_he': 'תיאור מעודכן',
            'feedback': 'Updated feedback',
            'scenario': 'Updated scenario',
            'level': 'advanced',
        }
        response = self.client.post(reverse('GitSection2'), data=post_data)
        self.assertEqual(response.status_code, 200)
        updated_exercise = Terminal_Exercises_Git_Commands.objects.get(id=self.exercise.id)
        self.assertEqual(updated_exercise.command, 'git status updated')
        self.assertEqual(updated_exercise.English_Description, 'Updated description')
        self.assertEqual(updated_exercise.level, 'advanced')

    def test_post_update_terminal_exercise_nonexistent_id_no_exception(self):
        post_data = {
            'update_terminal_exercise': 'true',
            'exercise_id': '999999',  # Nonexistent ID
            'command': 'git nothing',
            'description_en': 'Does not matter',
            'description_he': 'לא משנה',
            'feedback': 'No feedback',
            'scenario': 'No scenario',
            'level': 'basic',
        }
        response = self.client.post(reverse('GitSection2'), data=post_data)
        self.assertEqual(response.status_code, 200)  # Should not raise exception

    def test_post_delete_terminal_exercise_deletes_exercise(self):
        post_data = {
            'delete_terminal_exercise': 'true',
            'exercise_id': str(self.exercise.id),
        }
        response = self.client.post(reverse('GitSection2'), data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Terminal_Exercises_Git_Commands.objects.filter(id=self.exercise.id).exists())



from django.test import TestCase, Client
from django.urls import reverse
from GitExercises.models import GitSentence, GitHubSentence

class GitSection1ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('GitSection1')  # החליפי לשם ה-URL האמיתי שלך אם שונה
        # יצירת רשומות התחלתיות לבדיקה
        self.git_sentence = GitSentence.objects.create(sentence='Initial Git sentence')
        self.github_sentence = GitHubSentence.objects.create(sentence='Initial GitHub sentence')

    def test_get_request_renders_correctly(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Git_sentences', response.context)
        self.assertIn('GitHub_sentences', response.context)

    def test_post_add_git_sentence(self):
        response = self.client.post(self.url, {'add_git_sentence': '1', 'new_git_sentence': 'New Git sentence'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(GitSentence.objects.filter(sentence='New Git sentence').exists())

    def test_post_add_github_sentence(self):
        response = self.client.post(self.url, {'add_github_sentence': '1', 'new_github_sentence': 'New GitHub sentence'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(GitHubSentence.objects.filter(sentence='New GitHub sentence').exists())

    def test_post_update_git_sentence(self):
        response = self.client.post(self.url, {
            'update_git_sentence': '1',
            'git_sentence_id': self.git_sentence.id,
            'updated_git_sentence': 'Updated Git sentence'
        })
        self.assertEqual(response.status_code, 200)
        self.git_sentence.refresh_from_db()
        self.assertEqual(self.git_sentence.sentence, 'Updated Git sentence')

    def test_post_update_github_sentence(self):
        response = self.client.post(self.url, {
            'update_github_sentence': '1',
            'github_sentence_id': self.github_sentence.id,
            'updated_github_sentence': 'Updated GitHub sentence'
        })
        self.assertEqual(response.status_code, 200)
        self.github_sentence.refresh_from_db()
        self.assertEqual(self.github_sentence.sentence, 'Updated GitHub sentence')

    def test_post_delete_git_sentence(self):
        response = self.client.post(self.url, {
            'delete_git_sentence': '1',
            'git_sentence_id': self.git_sentence.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(GitSentence.objects.filter(id=self.git_sentence.id).exists())

    def test_post_delete_github_sentence(self):
        response = self.client.post(self.url, {
            'delete_github_sentence': '1',
            'github_sentence_id': self.github_sentence.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(GitHubSentence.objects.filter(id=self.github_sentence.id).exists())

from django.test import TestCase, Client
from django.urls import reverse
from GitExercises.models import Terminal_Exercises_Git_Commands

class GitSection2ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('GitSection2')  # עדכני לשם ה-URL שלך אם שונה
        self.exercise = Terminal_Exercises_Git_Commands.objects.create(
            command='git status',
            Hebrew_Command='git סטטוס',
            English_Description='Check the status',
            Hebrew_Description='בדוק את המצב',
            git_feedback='Good job',
            git_command_scenario='Scenario 1',
            level='easy'
        )

    def test_get_request_renders_correctly(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Terminal_Exercises', response.context)
        self.assertIn('Terminal_Exercises_form', response.context)
        self.assertIn('levels', response.context)

    def test_post_add_terminal_exercise(self):
        data = {
            'add_terminal_exercise': '1',
            'command': 'git commit',
            'Hebrew_Command': 'git קומי',
            'description_en': 'Commit changes',
            'description_he': 'שמור שינויים',
            'feedback': 'Well done',
            'scenario': 'Scenario 2',
            'level': 'medium'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Terminal_Exercises_Git_Commands.objects.filter(command='git commit').exists())

    def test_post_update_terminal_exercise(self):
        data = {
            'update_terminal_exercise': '1',
            'exercise_id': self.exercise.id,
            'command': 'git add .',
            'description_en': 'Add all files',
            'description_he': 'הוסף את כל הקבצים',
            'feedback': 'Added files',
            'scenario': 'Scenario updated',
            'level': 'hard'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.exercise.refresh_from_db()
        self.assertEqual(self.exercise.command, 'git add .')
        self.assertEqual(self.exercise.English_Description, 'Add all files')
        self.assertEqual(self.exercise.Hebrew_Description, 'הוסף את כל הקבצים')
        self.assertEqual(self.exercise.git_feedback, 'Added files')
        self.assertEqual(self.exercise.git_command_scenario, 'Scenario updated')
        self.assertEqual(self.exercise.level, 'hard')

    def test_post_delete_terminal_exercise(self):
        data = {
            'delete_terminal_exercise': '1',
            'exercise_id': self.exercise.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Terminal_Exercises_Git_Commands.objects.filter(id=self.exercise.id).exists())
