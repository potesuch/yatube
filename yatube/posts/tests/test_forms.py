import shutil
import tempfile
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from posts.models import Post, Group, Comment

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='testuser')
        cls.group = Group.objects.create(
            title='Заголовок_1',
            slug='first',
            description='Описание_1'
        )
        cls.post = Post.objects.create(
            text='Текст_1',
            author=cls.user,
            group=cls.group
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает запись в post."""
        post_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Текст_2',
            'group': 1,
            'image': uploaded
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), post_count+1)
        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': self.user.username})
        )
        self.assertTrue(
            Post.objects.filter(
                text='Текст_2',
                author=1,
                group=1,
                image='posts/small.gif'
            ).exists()
        )

    def test_edit_post(self):
        """Валидная форма редиактирует запись в post."""
        form_data = {
            'text': 'Текст_2',
            'group': ''
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': 1}),
            form_data
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': 1})
        )
        self.assertTrue(
            Post.objects.filter(
                pk=1,
                text='Текст_2',
                group=None
            )
        )

    def test_create_comment(self):
        """Валидная форма создает запись в comment"""
        comment_count = Comment.objects.count()
        form_data = {
            'text': 'Комментарий_1'
        }
        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': 1}),
            form_data,
            follow=True
        )
        self.assertEqual(Comment.objects.count(), comment_count+1)
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': 1})
        )
        self.assertTrue(
            Comment.objects.filter(
                post=1,
                author=1,
                text='Комментарий_1'
            ).exists()
        )
