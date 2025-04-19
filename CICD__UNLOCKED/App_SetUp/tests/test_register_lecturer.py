from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail

User = get_user_model()


class LecturerRegistrationTests(TestCase):
    """
    בדיקות יחידה לתהליך ההרשמה של מרצה למערכת
    """

    def setUp(self):
        """
        הכנת נתוני הבדיקה
        """
        # יצירת משתמש אדמין שיוכל לאשר בקשות
        self.admin_user = User.objects.create_user(
            username='admin_test',
            email='admin_test@example.com',
            password='password123',
            is_admin=True,
            is_active=True
        )

        # נתונים לרישום מרצה חדש
        self.new_lecturer_data = {
            'username': 'new_lecturer',
            'email': 'new_lecturer@example.com',
            'password1': 'ComplexPass123!',  # שימו לב - סיסמה חזקה נדרשת
            'password2': 'ComplexPass123!',  # אימות סיסמה
            'first_name': 'מרצה',
            'last_name': 'חדש',
            'role': 'lecturer'  # הפרמטר שמגדיר הרשמה כמרצה
        }

        # הכנת הקליינט לביצוע בקשות
        self.client = Client()

        # URLs לשימוש בבדיקות
        self.register_url = reverse('register')  # שם הנתיב ב-urls.py לדף ההרשמה
        self.login_url = reverse('login_view')  # שם הנתיב לדף ההתחברות
        self.admin_url = reverse('admin')  # שם הנתיב לדף האדמין
        self.handle_lecturer_request_url = reverse('handle_lecturer_request')  # שם הנתיב לטיפול בבקשות מרצה

    def test_lecturer_registration_form_display(self):
        """
        בדיקה שטופס ההרשמה מוצג כראוי
        """
        response = self.client.get(self.register_url)

        # בדיקה שהדף נטען בהצלחה
        self.assertEqual(response.status_code, 200)

        # בדיקה שהטופס מכיל את השדות הנדרשים
        self.assertContains(response, 'username')
        self.assertContains(response, 'email')
        self.assertContains(response, 'password')
        self.assertContains(response, 'role')
        self.assertContains(response, 'lecturer')  # אפשרות להירשם כמרצה

    def test_successful_lecturer_registration(self):
        """
        בדיקה שהרשמת מרצה חדש מצליחה ויוצרת משתמש מרצה לא פעיל
        """
        response = self.client.post(self.register_url, self.new_lecturer_data)

        # בדיקה שההרשמה הסתיימה בהצלחה
        self.assertEqual(response.status_code, 200)

        # בדיקה שנוצר משתמש חדש מסוג מרצה
        self.assertTrue(User.objects.filter(username='new_lecturer').exists())
        new_user = User.objects.get(username='new_lecturer')

        # בדיקה שהמשתמש הוא אכן מרצה
        self.assertTrue(new_user.is_lecturer)

        # בדיקה שהמשתמש לא פעיל (ממתין לאישור)
        self.assertFalse(new_user.is_active)

        # בדיקה שמופיעה הודעה מתאימה
        self.assertContains(response, 'בקשתך לחשבון מרצה')

    def test_duplicate_email_registration(self):
        """
        בדיקה שלא ניתן להירשם עם אותה כתובת אימייל פעמיים
        """
        # יצירת משתמש ראשון
        self.client.post(self.register_url, self.new_lecturer_data)

        # ניסיון רישום עם אותו אימייל
        duplicate_data = self.new_lecturer_data.copy()
        duplicate_data['username'] = 'another_lecturer'  # שם משתמש שונה

        response = self.client.post(self.register_url, duplicate_data)

        # בדיקה שההרשמה נכשלה
        self.assertEqual(response.status_code, 200)

        # בדיקה שמופיעה הודעת שגיאה מתאימה
        self.assertContains(response, 'כתובת הדואר האלקטרוני כבר רשומה במערכת')

        # בדיקה שלא נוצר משתמש נוסף
        self.assertFalse(User.objects.filter(username='another_lecturer').exists())

    def test_duplicate_username_registration(self):
        """
        בדיקה שלא ניתן להירשם עם אותו שם משתמש פעמיים
        """
        # יצירת משתמש ראשון
        self.client.post(self.register_url, self.new_lecturer_data)

        # ניסיון רישום עם אותו שם משתמש
        duplicate_data = self.new_lecturer_data.copy()
        duplicate_data['email'] = 'another_email@example.com'  # אימייל שונה

        response = self.client.post(self.register_url, duplicate_data)

        # בדיקה שההרשמה נכשלה
        self.assertEqual(response.status_code, 200)

        # בדיקה שמופיעה הודעת שגיאה מתאימה (או באנגלית או בעברית)
        self.assertTrue(
            'שם המשתמש כבר קיים במערכת' in response.content.decode() or
            'A user with that username already exists' in response.content.decode(),
            "לא נמצאה הודעת שגיאה מתאימה עבור שם משתמש כפול"
        )

    def test_invalid_form_submission(self):
        """
        בדיקה שטופס לא תקין מציג הודעות שגיאה מתאימות
        """
        # נתונים חסרים בטופס
        invalid_data = {
            'username': 'new_lecturer',
            'email': '',  # אימייל חסר
            'password1': 'ComplexPass123!',
            'password2': 'DifferentPass123!',  # סיסמה לא תואמת
            'role': 'lecturer'
        }

        response = self.client.post(self.register_url, invalid_data)

        # בדיקה שההרשמה נכשלה
        self.assertEqual(response.status_code, 200)

        # בדיקה שמופיעה הודעת שגיאה
        self.assertContains(response, 'אנא ודא/י כי כל השדות מולאו כראוי')

        # בדיקה שלא נוצר משתמש חדש
        self.assertFalse(User.objects.filter(username='new_lecturer').exists())

    def test_admin_can_approve_lecturer(self):
        """
        בדיקה שמנהל יכול לאשר בקשת מרצה
        """
        # יצירת בקשת מרצה חדשה
        self.client.post(self.register_url, self.new_lecturer_data)
        new_lecturer = User.objects.get(username='new_lecturer')

        # התחברות כאדמין
        self.client.login(username='admin_test', password='password123')

        # בדיקה שהבקשה מופיעה בדף האדמין
        admin_response = self.client.get(self.admin_url)
        self.assertContains(admin_response, 'new_lecturer@example.com')

        # אישור בקשת המרצה
        approve_response = self.client.post(self.handle_lecturer_request_url, {
            'user_email': 'new_lecturer@example.com',
            'action': 'approve'
        })

        # בדיקה שהמשתמש הופנה חזרה לדף האדמין
        self.assertRedirects(approve_response, self.admin_url)

        # בדיקה שהמרצה הפך לפעיל
        new_lecturer.refresh_from_db()
        self.assertTrue(new_lecturer.is_active)

        # בדיקה שנשלח מייל אישור
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('חשבון המרצה שלך אושר', mail.outbox[0].subject)

    def test_admin_can_reject_lecturer(self):
        """
        בדיקה שמנהל יכול לדחות בקשת מרצה
        """
        # יצירת בקשת מרצה חדשה
        self.client.post(self.register_url, self.new_lecturer_data)

        # התחברות כאדמין
        self.client.login(username='admin_test', password='password123')

        # דחיית בקשת המרצה
        reject_response = self.client.post(self.handle_lecturer_request_url, {
            'user_email': 'new_lecturer@example.com',
            'action': 'reject'
        })

        # בדיקה שהמשתמש הופנה חזרה לדף האדמין
        self.assertRedirects(reject_response, self.admin_url)

        # בדיקה שהמרצה נמחק מהמערכת
        self.assertFalse(User.objects.filter(username='new_lecturer').exists())

        # בדיקה שנשלח מייל דחייה
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('בקשתך להירשם כמרצה סורבה', mail.outbox[0].subject)

    def test_inactive_lecturer_cant_login(self):
        """
        בדיקה שמרצה לא פעיל לא יכול להתחבר למערכת
        """
        # יצירת בקשת מרצה חדשה
        self.client.post(self.register_url, self.new_lecturer_data)

        # ניסיון התחברות כמרצה לא פעיל
        login_response = self.client.post(self.login_url, {
            'username': 'new_lecturer',
            'password': 'ComplexPass123!'
        })

        # בדיקה שההתחברות נכשלה (לא מועבר לדף המרצה)
        self.assertEqual(login_response.status_code, 200)

        # בדיקה שהמשתמש לא מחובר
        user = login_response.wsgi_request.user
        self.assertFalse(user.is_authenticated)