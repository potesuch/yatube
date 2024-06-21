from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class UserURLTest(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create(username='testuser')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_exists_at_desired_location_for_anonymous(self):
        """Страницы доступны анонимному пользователю."""
        urls = (
            '/auth/signup/',
            '/auth/login/',
            '/auth/password_reset/',
            '/auth/password_reset/done/',
            '/auth/reset/test-uidb64/test-token/',
            '/auth/reset/done/'
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_exists_at_desired_location_for_authorized(self):
        """Страницы доступны авторизованному пользователю."""
        urls = (
            '/auth/password_change/',
            '/auth/password_change/done/',
            '/auth/logout/',
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_redirect_anonymous(self):
        """Страницы перенаправляют анонимного пользователя."""
        redirects = {
        #    '/auth/logout/': '/auth/login/?next=/auth/logout/',
            '/auth/password_change/': '/auth/login/?next=/auth/password_change/',
            '/auth/password_change/done/': '/auth/login/?next=/auth/password_change/done/',
        }
        for url, redirect_url in redirects.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_urls_uses_correct_template(self):
        """URL-адреса используют соответствующие шаблоны."""
        url_names_templates = {
            '/auth/signup/': 'users/signup.html',
            '/auth/login/': 'users/login.html',
            '/auth/password_reset/': 'users/password_reset_form.html',
            '/auth/password_reset/done/': 'users/password_reset_done.html',
            '/auth/reset/test-uidb64/test-token/': 'users/password_reset_confirm.html',
            '/auth/reset/done/': 'users/password_reset_complete.html',
            '/auth/password_change/': 'users/password_change_form.html',
            '/auth/password_change/done/': 'users/password_change_done.html',
            '/auth/logout/': 'users/logged_out.html',
        }
        for url, template in url_names_templates.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
