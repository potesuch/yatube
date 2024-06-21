import shutil
import tempfile
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django import forms
from django.core.cache import cache
from posts.models import Post, Group

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='testuser')
        cls.author = User.objects.create(username='testauthor')
        cls.group = Group.objects.create(
            title='Заголовок',
            slug='test-slug-1',
            description='Описание',
        )
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        Post.objects.create(
            text='Текст_1',
            author=cls.author,
            group=cls.group,
            image=cls.uploaded
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author_client = Client()
        self.author_client.force_login(self.author)
        cache.clear()

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': (
                reverse('posts:group_list', kwargs={'slug': 'test-slug-1'})
            ),
            'posts/profile.html': (
                reverse('posts:profile', kwargs={'username': 'testauthor'})
            ),
            'posts/post_detail.html': (
                reverse('posts:post_detail', kwargs={'post_id': 1})
            ),
            'posts/post_form.html': reverse('posts:post_create'),
            'posts/post_form.html': (
                reverse('posts:post_edit', kwargs={'post_id': 1})
            ),
        }
        for template, reverse_name in templates_page_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.author_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author
        post_group_0 = first_object.group
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, 'Текст_1')
        self.assertEqual(post_author_0, self.author)
        self.assertEqual(post_group_0, self.group)
        self.assertEqual(post_image_0, 'posts/small.gif')

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным шаблоном."""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test-slug-1'})
        )
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author
        post_group_0 = first_object.group
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, 'Текст_1')
        self.assertEqual(post_author_0, self.author)
        self.assertEqual(post_group_0, self.group)
        self.assertEqual(post_image_0, 'posts/small.gif')
        self.assertQuerysetEqual(
            response.context['page_obj'],
            Post.objects.filter(group=self.group)
        )

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': 'testauthor'})
        )
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author
        post_group_0 = first_object.group
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, 'Текст_1')
        self.assertEqual(post_author_0, self.author)
        self.assertEqual(post_group_0, self.group)
        self.assertEqual(post_image_0, 'posts/small.gif')
        self.assertQuerysetEqual(
            response.context['page_obj'],
            Post.objects.filter(author=self.author)
        )

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': 1})
        )
        post_object = response.context.get('post')
        post_text = post_object.text
        post_author = post_object.author
        post_group = post_object.group
        post_image = post_object.image
        self.assertEqual(post_text, 'Текст_1')
        self.assertEqual(post_author, self.author)
        self.assertEqual(post_group, self.group)
        self.assertEqual(post_image, 'posts/small.gif')

    def test_post_create_page_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом"""
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        response = self.authorized_client.get(reverse('posts:post_create'))
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_page_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        response = self.author_client.get(
            reverse('posts:post_edit', kwargs={'post_id': 1})
        )
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_creating_is_correct(self):
        """Проверка корректности отображения созданного поста."""
        group = Group.objects.create(
            title='Заголовок_2',
            slug='test-slug-2',
            description='Описание1',
        )
        post = Post.objects.create(
            text='Текст_2',
            author=self.author,
            group=group
        )
        response_index = self.authorized_client.get(reverse('posts:index'))
        response_group_list_1 = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test-slug-2'})
        )
        response_group_list_2 = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test-slug-1'})
        )
        response_profile = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': 'testauthor'})
        )
        self.assertIn(post, response_index.context['page_obj'])
        self.assertIn(post, response_group_list_1.context['page_obj'])
        self.assertNotIn(post, response_group_list_2.context['page_obj'])
        self.assertIn(post, response_profile.context['page_obj'])

    def test_post_cache_index(self):
        """Проверка кэширования index."""
        post = Post.objects.create(
            text='Кэш пост',
            author=self.user
        )
        response_1 = self.authorized_client.get(reverse('posts:index'))
        self.assertIn(post.text, response_1.content.decode())
        post.delete()
        response_2 = self.authorized_client.get(reverse('posts:index'))
        self.assertIn(post.text, response_2.content.decode())
        cache.clear()
        response_3 = self.authorized_client.get(reverse('posts:index'))
        self.assertNotIn(post.text, response_3.content.decode())

    def test_authorized_user_can_follow_and_unfollow(self):
        """Авторизованный пользователь может подписываться и отписываться."""
        user = User.objects.get(username='testuser')
        response_1 = self.authorized_client.get(
            reverse('posts:profile_follow', kwargs={'username': 'testauthor'})
        )
        self.assertRedirects(
            response_1, reverse(
                'posts:profile',
                kwargs={'username': 'testauthor'}
            )
        )
        self.assertTrue(user.follower.filter(following=2).exists())
        response_2 = self.authorized_client.get(
            reverse('posts:profile_unfollow', kwargs={'username': 'testauthor'})
        )
        self.assertRedirects(
            response_2,
            reverse('posts:profile', kwargs={'username': 'testauthor'})
        )
        self.assertFalse(user.follower.filter(following=2).exists())
