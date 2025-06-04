from django.test import TestCase, RequestFactory
from App_SetUp.models import LogoSettings
from App_SetUp.context_processors import logo_settings_context
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth import get_user_model
User = get_user_model()


class LogoSettingsTests(TestCase):
    def setUp(self):
        self.logo = LogoSettings.objects.create(
            text="Test Logo",
            font_family="Arial",
            font_size=24,
            gradient_from="#123456",
            gradient_to="#abcdef"
        )
        self.factory = RequestFactory()

    def test_logo_settings_saved_correctly(self):
        logo = LogoSettings.objects.first()
        self.assertEqual(logo.text, "Test Logo")
        self.assertEqual(logo.font_family, "Arial")
        self.assertEqual(logo.font_size, 24)
        self.assertEqual(logo.gradient_from, "#123456")
        self.assertEqual(logo.gradient_to, "#abcdef")

    def test_context_processor_returns_logo_settings(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()  # לא מחובר
        context = logo_settings_context(request)

        self.assertIn('logo_settings', context)
        logo = context['logo_settings']
        self.assertEqual(logo.text, "Test Logo")
        self.assertEqual(context['background_color'], "#2b2b3c")

    def test_context_processor_background_for_admin(self):
        user = User.objects.create_user(username='adminuser', password='1234')
        user.is_admin = True  # מניח שאתה מוסיף את זה בדגם CustomUser
        user.save()

        request = self.factory.get('/')
        request.user = user
        context = logo_settings_context(request)

        self.assertEqual(context['background_color'], "#f4f7fb")

    def test_context_processor_background_for_student(self):
        user = User.objects.create_user(username='studentuser', password='1234')
        user.is_student = True
        user.save()

        request = self.factory.get('/')
        request.user = user
        context = logo_settings_context(request)

        self.assertEqual(context['background_color'], "#0a0e1a")

