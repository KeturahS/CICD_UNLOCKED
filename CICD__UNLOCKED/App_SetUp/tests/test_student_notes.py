from django.test import TestCase, Client
from django.urls import reverse
from App_SetUp.models import User, StudentNote

class StudentNotesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.student_user = User.objects.create_user(
            username='student', password='pass1234', is_student=True
        )
        self.client.login(username='student', password='pass1234')

    def test_student_can_submit_note(self):
        response = self.client.post(reverse("add_student_note"), {
            "module": "Git",
            "content": "זוהי הערה לדוגמה."
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(StudentNote.objects.filter(student=self.student_user, module="Git").exists())

    def test_notes_appear_in_view_notes(self):
        StudentNote.objects.create(student=self.student_user, module="Docker", content="בדיקה")
        response = self.client.get(reverse("view_student_notes"))
        self.assertContains(response, "בדיקה")
        self.assertContains(response, "Docker")

    def test_student_note_module_saved_correctly(self):
        self.client.post(reverse("add_student_note"), {
            "module": "Jenkins",
            "content": "בדיקת הערה למודול Jenkins"
        })
        note = StudentNote.objects.filter(student=self.student_user).latest("created_at")
        self.assertEqual(note.module, "Jenkins")
