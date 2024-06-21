import shutil
import tempfile
from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from users.forms import CreationForm

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
User = get_user_model()

@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class UserFormTest(TestCase):
    def setUp(self):
        self.client = Client()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_create_user(self):
        user_count = User.objects.count()
        form_data = {
            'username': 'user',
            'email': 'test@test.te',
            'password1': 'Qazwsxedc1.',
            'password2': 'Qazwsxedc1.'
        }
        response = self.client.post(
            reverse('users:signup'),
            form_data,
            follow=True
        )
        self.assertEqual(User.objects.count(), user_count+1)
        self.assertRedirects(response, reverse('posts:index'))
        self.assertTrue(
            User.objects.filter(
                username='user',
                email='test@test.te'
            ).exists()
        )
