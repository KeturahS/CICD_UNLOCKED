from django.test import TestCase, Client
from django.urls import reverse
from QA.models import FAQ

class QAPageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.faq1 = FAQ.objects.create(question="What is Django?", answer="A web framework")
        self.faq2 = FAQ.objects.create(question="What is Python?", answer="A programming language")


    def test_get_all_faqs(self):
        response = self.client.get(reverse('qa:QA_Page'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.faq1, response.context['faqs'])
        self.assertIn(self.faq2, response.context['faqs'])
        self.assertTemplateUsed(response, 'QA_Page.html')

    def test_post_search_query(self):
        response = self.client.post(reverse('qa:QA_Page'), {'search_query': 'django'})
        self.assertContains(response, "What is Django?")
        self.assertNotContains(response, "What is Python?")
        self.assertEqual(list(response.context['filtered_faqs']), [self.faq1])



class HandleFAQTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.faq = FAQ.objects.create(question="Old Question", answer="Old Answer")

    def test_add_faq(self):
        response = self.client.post(reverse('qa:handle_faq'), {
            'add_QA': 'true',
            'question': 'New Question',
            'answer': 'New Answer'
        })
        self.assertTrue(FAQ.objects.filter(question='New Question').exists())

    def test_delete_faq(self):
        response = self.client.post(reverse('qa:handle_faq'), {
            'delete_QA': 'true',
            'faq_id': self.faq.id
        })
        self.assertFalse(FAQ.objects.filter(id=self.faq.id).exists())

    def test_update_faq(self):
        response = self.client.post(reverse('qa:handle_faq'), {
            'update_QA': 'true',
            'faq_id': self.faq.id,
            'question': 'Updated Question',
            'answer': 'Updated Answer'
        })
        self.faq.refresh_from_db()
        self.assertEqual(self.faq.question, 'Updated Question')
        self.assertEqual(self.faq.answer, 'Updated Answer')

    def test_template_used(self):
        response = self.client.get(reverse('qa:handle_faq'))
        self.assertTemplateUsed(response, 'LecturerPages/lecturer_manage_FAQ.html')
