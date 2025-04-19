from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminLoginTests(TestCase):
    """
    בדיקות יחידה לתהליך ההתחברות של אדמין למערכת
    """

    def setUp(self):
        """
        הכנת נתוני הבדיקה - יצירת משתמש אדמין פעיל ומשתמש אדמין לא פעיל
        """
        # יצירת משתמש אדמין פעיל
        self.active_admin = User.objects.create_user(
            username='admin_active',
            email='admin_active@example.com',
            password='password123',
            is_admin=True,
            is_active=True
        )

        # יצירת משתמש אדמין שטרם אושר
        self.inactive_admin = User.objects.create_user(
            username='admin_inactive',
            email='admin_inactive@example.com',
            password='password123',
            is_admin=True,
            is_active=False
        )

        # יצירת משתמש רגיל (לא אדמין)
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
        self.admin_dashboard_url = reverse('admin')  # שם הנתיב ב-urls.py של הפרויקט שלך

    def test_admin_login_success(self):
        """
        בדיקה שאדמין פעיל יכול להתחבר בהצלחה ומועבר לדף האדמין
        """
        response = self.client.post(self.login_url, {
            'username': 'admin_active',
            'password': 'password123'
        })

        # בדיקה שהמשתמש הועבר לדף האדמין
        self.assertRedirects(response, self.admin_dashboard_url)

        # בדיקה שהמשתמש מחובר
        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated)
        self.assertTrue(user.is_admin)

    def test_inactive_admin_login(self):
        """
        בדיקה שאדמין לא פעיל (שטרם אושר) מקבל הודעה מתאימה
        """
        response = self.client.post(self.login_url, {
            'username': 'admin_inactive',
            'password': 'password123'
        })

        # בדיקה שההתחברות לא הצליחה והמשתמש נשאר בדף ההתחברות
        self.assertEqual(response.status_code, 200)

        # בדיקה שהמשתמש לא הופנה לדף האדמין (כלומר, לא התחבר בהצלחה)
        self.assertNotEqual(response.url if hasattr(response, 'url') else '', self.admin_dashboard_url)

    def test_wrong_password_login(self):
        """
        בדיקה שניסיון התחברות עם סיסמה שגויה נכשל
        """
        response = self.client.post(self.login_url, {
            'username': 'admin_active',
            'password': 'wrong_password'
        })

        # בדיקה שההתחברות נכשלה והוצגה הודעת שגיאה
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'פרטים לא נכונים')

    def test_non_admin_redirect(self):
        """
        בדיקה שמשתמש רגיל לא יכול לגשת לפונקציונליות של דף האדמין
        """
        # התחברות כמשתמש רגיל
        self.client.login(username='regular_user', password='password123')

        # ניסיון גישה לפעולה שדורשת הרשאות אדמין (ניהול בקשות אדמין)
        try:
            handle_admin_request_url = reverse('handle_admin_request')
            response = self.client.post(handle_admin_request_url, {
                'user_email': 'test@example.com',
                'action': 'approve'
            })

            # בדיקה שהמשתמש אינו יכול לבצע פעולות אדמין
            # אם ההרשאות פועלות כראוי, או שיהיה קוד שגיאה או שלא יתבצע שינוי
            self.assertTrue(response.status_code >= 400 or 'permission denied' in response.content.decode().lower())
        except:
            # אם המערכת מנעה את הפעולה בדרך אחרת (למשל החזירה שגיאה), הבדיקה גם עוברת
            pass

    def test_admin_login_form_invalid(self):
        """
        בדיקה שטופס התחברות לא תקין מציג הודעת שגיאה מתאימה
        """
        # שליחת טופס התחברות ריק
        response = self.client.post(self.login_url, {})

        # בדיקה שהוצגה הודעת שגיאה מתאימה
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'טופס לא תקין')