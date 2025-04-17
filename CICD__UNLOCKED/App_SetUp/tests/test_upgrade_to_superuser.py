from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

User = get_user_model()


class AdminUpgradeTests(TestCase):

    def setUp(self):
        self.client = Client()
        # יצירת משתמש רגיל
        self.user = User.objects.create_user(
            username='regularAdmin',
            email='regular@example.com',
            password='password123',
            is_active=True,
            is_admin = True
        )
        # יצירת משתמש מנהל מחובר
        self.admin_user = User.objects.create_user(
            username='Superadminuser',
            email='admin@example.com',
            password='adminpass',
            is_active=True,
            is_admin=True,
            is_superuser=True,
            is_staff=True
        )

    def test_upgrade_admin(self):
        # כניסה עם המשתמש המנהל
        self.client.login(username= 'Superadminuser', email='admin@example.com', password='adminpass')

        # בקשת POST לשדרוג המשתמש הרגיל למנהל
        response = self.client.post(reverse('upgrade_admin'), {
            'admin_email': 'regular@example.com'
        })

        # טוען את המשתמש לאחר השדרוג
        self.user.refresh_from_db()

        # בודק שהמאפיינים של המשתמש השתנו כראוי
        self.assertTrue(self.user.is_admin)
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.user.is_superuser)
        self.assertTrue(self.user.is_staff)

        # בודק שהדף מפנה חזרה למנהל
        self.assertRedirects(response, reverse('manage_admins'))
