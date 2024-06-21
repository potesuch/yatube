from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Post, Group

User = get_user_model()


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='testuser')
        cls.group = Group.objects.create(
            title='Заголовок',
            slug='test-slug',
            description='Описание',
        )
        Post.objects.bulk_create(
            [Post(
                text=f'Текст_{i}',
                author=cls.user,
                group=cls.group,
            ) for i in range(13)]
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.reverse_names = (
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': 'test-slug'}),
            reverse('posts:profile', kwargs={'username': 'testuser'}),
        )

    def test_first_page_contains_ten_records(self):
        """Первая страница содержит 10 записей."""
        for name in self.reverse_names:
            with self.subTest(name=name):
                response = self.authorized_client.get(name)
                self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_three_records(self):
        """Вторая страница содержит 3 записи."""
        for name in self.reverse_names:
            with self.subTest(name=name):
                response = self.authorized_client.get(name+'?page=2')
                self.assertEqual(len(response.context['page_obj']), 3)