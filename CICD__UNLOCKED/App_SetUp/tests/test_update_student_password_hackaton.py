from django.test import TestCase
from django.contrib.auth import get_user_model
from App_SetUp.forms import StudentProfileUpdateForm
from App_SetUp.models import StudentProfile
from datetime import date, timedelta

User = get_user_model()

class StudentPasswordUpdateFormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='student1',
            email='student@example.com',
            password='OldPassword123',
            first_name='Test',
            last_name='User',
            is_student=True
        )
        self.profile = StudentProfile.objects.create(
            user=self.user,
            institution='SCE',
            target_completion_date=date.today() + timedelta(days=30)
        )

    def test_valid_password_update(self):
        form_data = {
            'institution': 'SCE',
            'target_completion_date': date.today() + timedelta(days=30),
            'first_name': 'NewName',
            'last_name': 'User',
            'email': 'newemail@example.com',
            'new_password': 'NewPass123!'
        }
        form = StudentProfileUpdateForm(data=form_data, instance=self.profile, user=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(self.user.check_password('NewPass123!'))

    def test_password_too_short(self):
        form_data = {
            'institution': 'SCE',
            'target_completion_date': date.today() + timedelta(days=30),
            'first_name': 'NewName',
            'last_name': 'User',
            'email': 'newemail@example.com',
            'new_password': '123'
        }
        form = StudentProfileUpdateForm(data=form_data, instance=self.profile, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("הסיסמה חייבת להיות לפחות 8 תווים", form.non_field_errors())

    def test_password_digits_only(self):
        form_data = {
            'institution': 'SCE',
            'target_completion_date': date.today() + timedelta(days=30),
            'first_name': 'NewName',
            'last_name': 'User',
            'email': 'newemail@example.com',
            'new_password': '12345678'
        }
        form = StudentProfileUpdateForm(data=form_data, instance=self.profile, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("הסיסמה לא יכולה להכיל רק מספרים", form.non_field_errors())

    def test_password_same_as_username(self):
        form_data = {
            'institution': 'SCE',
            'target_completion_date': date.today() + timedelta(days=30),
            'first_name': 'NewName',
            'last_name': 'User',
            'email': 'newemail@example.com',
            'new_password': 'student1'
        }
        form = StudentProfileUpdateForm(data=form_data, instance=self.profile, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("הסיסמה לא יכולה להיות זהה לשם המשתמש או הדואר אלקטרוני", form.non_field_errors())

    def test_no_password_field_provided(self):
        form_data = {
            'institution': 'SCE',
            'target_completion_date': date.today() + timedelta(days=30),
            'first_name': 'NewName',
            'last_name': 'User',
            'email': 'newemail@example.com',
            'new_password': ''
        }
        form = StudentProfileUpdateForm(data=form_data, instance=self.profile, user=self.user)
        self.assertTrue(form.is_valid())
        old_hash = self.user.password
        form.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.password, old_hash)  # password didn't change
