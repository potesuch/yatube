from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.models import Post, Group

User = get_user_model()


class PostURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='testuser')
        cls.author = User.objects.create(username='testauthor')
        Post.objects.create(
            text='Тестовый текст',
            author=cls.author
        )
        Group.objects.create(
            title='Тестовый заголовок',
            slug='test-slug',
            description='Тестовое описание'
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostURLTest.user)
        self.author_client = Client()
        self.author_client.force_login(PostURLTest.author)

    def test_urls_exists_at_desired_location_for_anonymous(self):
        """Страницы доступны анонимному пользователю."""
        urls = (
            '/',
            '/group/test-slug/',
            '/profile/testuser/',
            '/posts/1/',
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_exists_at_desired_location_for_authorized(self):
        """Страницы доступны для авторизованного пользователя."""
        urls = (
            '/create/',
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_exist_at_desired_location_for_author(self):
        """Страницы доступны для пользователя автора."""
        urls = (
            '/posts/1/edit/',
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_redirect_anonymous(self):
        """Страницы перенаправляют анонимного пользователя."""
        redirects = {
            '/create/': '/auth/login/?next=/create/',
            '/posts/1/edit/': '/auth/login/?next=/posts/1/edit/',
            '/posts/1/comment/': '/auth/login/?next=/posts/1/comment/',
        }
        for url, redirect_url in redirects.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_urls_redirect_authorized(self):
        """Страницы перенаправляют авторизованного пользователя."""
        redirects = {
            '/posts/1/edit/': '/posts/1/',
        }
        for url, redirect_url in redirects.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        url_names_templates = {
            '/': 'posts/index.html',
            '/group/test-slug/': 'posts/group_list.html',
            '/profile/testuser/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
            '/create/': 'posts/post_form.html',
            '/posts/1/edit/': 'posts/post_form.html',
        }
        for url, template in url_names_templates.items():
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_unexisting_page(self):
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, 'core/404.html')
