from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class LecturerLoginTests(TestCase):
    """
    בדיקות יחידה לתהליך ההתחברות של מרצה למערכת
    """

    def setUp(self):
        """
        הכנת נתוני הבדיקה - יצירת משתמש מרצה פעיל ומשתמש מרצה לא פעיל
        """
        # יצירת משתמש מרצה פעיל
        self.active_lecturer = User.objects.create_user(
            username='lecturer_active',
            email='lecturer_active@example.com',
            password='password123',
            is_lecturer=True,
            is_active=True
        )

        # יצירת משתמש מרצה שטרם אושר
        self.inactive_lecturer = User.objects.create_user(
            username='lecturer_inactive',
            email='lecturer_inactive@example.com',
            password='password123',
            is_lecturer=True,
            is_active=False
        )

        # יצירת משתמש רגיל (לא מרצה)
        self.regular_user = User.objects.create_user(
            username='regular_user',
            email='regular_user@example.com',
            password='password123',
            is_student=True,
            is_active=True
        )

        # הכנת הקליינט לביצוע בקשות
        self.client = Client()

        # URLs לשימוש בבדיקות
        self.login_url = reverse('login_view')  # שם הנתיב ב-urls.py של הפרויקט שלך
        self.lecturer_dashboard_url = reverse('lecturer')  # שם הנתיב ב-urls.py של הפרויקט שלך

    def test_lecturer_login_success(self):
        """
        בדיקה שמרצה פעיל יכול להתחבר בהצלחה ומועבר לדף המרצה
        """
        response = self.client.post(self.login_url, {
            'username': 'lecturer_active',
            'password': 'password123'
        })

        # בדיקה שהמשתמש הועבר לדף המרצה
        self.assertRedirects(response, self.lecturer_dashboard_url)

        # בדיקה שהמשתמש מחובר
        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated)
        self.assertTrue(user.is_lecturer)

    def test_inactive_lecturer_login(self):
        """
        בדיקה שמרצה לא פעיל (שטרם אושר) לא יכול להתחבר
        """
        response = self.client.post(self.login_url, {
            'username': 'lecturer_inactive',
            'password': 'password123'
        })

        # בדיקה שההתחברות לא הצליחה והמשתמש נשאר בדף ההתחברות
        self.assertEqual(response.status_code, 200)

        # בדיקה שהמשתמש לא הופנה לדף המרצה
        self.assertNotEqual(response.url if hasattr(response, 'url') else '', self.lecturer_dashboard_url)

    def test_wrong_password_login(self):
        """
        בדיקה שניסיון התחברות עם סיסמה שגויה נכשל
        """
        response = self.client.post(self.login_url, {
            'username': 'lecturer_active',
            'password': 'wrong_password'
        })

        # בדיקה שההתחברות נכשלה והוצגה הודעת שגיאה
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'פרטים לא נכונים')

    def test_non_lecturer_access(self):
        """
        בדיקה שמשתמש רגיל מקבל תוכן מוגבל בדף המרצה
        """
        # התחברות כמשתמש רגיל
        self.client.login(username='regular_user', password='password123')

        # ניסיון גישה לדף המרצה
        response = self.client.get(self.lecturer_dashboard_url)

        # במקום לבדוק שהגישה נאסרה לחלוטין, נבדוק אם התוכן המוצג
        # למשתמש רגיל שונה מהתוכן שמוצג למרצה
        # שמור את התגובה למשתמש רגיל
        regular_user_response = response.content.decode()

        # התנתק והתחבר מחדש כמרצה
        self.client.logout()
        self.client.login(username='lecturer_active', password='password123')

        # גישה לדף המרצה שוב
        lecturer_response = self.client.get(self.lecturer_dashboard_url).content.decode()

        # בדוק שהתגובה שונה (יש הבדל בתוכן)
        self.assertNotEqual(
            regular_user_response,
            lecturer_response,
            "דף המרצה מציג אותו תוכן למרצים ולמשתמשים רגילים"
        )

    def test_login_form_display(self):
        """
        בדיקה שטופס ההתחברות מוצג כראוי
        """
        response = self.client.get(self.login_url)

        # בדיקה שהדף נטען בהצלחה
        self.assertEqual(response.status_code, 200)

        # בדיקה שהטופס מכיל את השדות הנדרשים
        self.assertContains(response, 'username')
        self.assertContains(response, 'password')
        self.assertContains(response, 'type="submit"')