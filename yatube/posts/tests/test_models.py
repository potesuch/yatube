from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Post, Group

User = get_user_model()


class PostModelTest(TestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='test')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='test-group',
            description='Тестовое описание'
        )
        cls.post = Post.objects.create(
            text='Т'*100,
            author=cls.user,
            group=cls.group
        )

    def test_models_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__"""
        post = PostModelTest.post
        post_str = post
        self.assertEqual(f'{post_str}', 'Т'*15)
        group = PostModelTest.group
        group_str = group
        self.assertEqual(f'{group_str}', f'Группа: {group.title} - {group.description}')

    def test_verbose_name(self):
        """verbose_name в полях совпадают с ожидаемым."""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value
                )

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'Введите текст поста',
            'group': 'Выберите группу'
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value
                )