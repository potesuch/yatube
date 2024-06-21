from http import HTTPStatus
from django.test import Client, TestCase


class CoreViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_error_page(self):
        """Проверка page_not_found"""
        response = self.client.get('/unexisting-page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, 'core/404.html')