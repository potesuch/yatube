from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django import forms
from django.urls import reverse

User = get_user_model()


class UserViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            'users/logged_out.html': reverse('users:logout'),
            'users/signup.html': reverse('users:signup'),
            'users/login.html': reverse('users:login'),
            'users/password_reset_form.html': reverse(
                'users:password_reset_form'
            ),
            'users/password_reset_done.html': reverse(
                'users:password_reset_done'
            ),
            'users/password_reset_confirm.html': reverse(
                'users:password_reset_confirm',
                kwargs={'uidb64': 'test_uidb64', 'token': 'test_token'}
            ),
            'users/password_reset_complete.html': reverse(
                'users:password_reset_complete'
            ),
            'users/password_change_form.html': reverse(
                'users:password_change_form'
            ),
            'users/password_change_done.html': reverse(
                'users:password_change_done'
            ),
        }
        for template, reverse_name in templates_page_names.items():
            with self.subTest(reverse_name=reverse_name):
                self.authorized_client.force_login(self.user) # Оптимизировать!!
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_signup_page_show_correct_context(self):
        """Шаблон signup сформирован с правильным контекстом."""
        form_fields = {
            'username': forms.fields.CharField,
            'email': forms.fields.EmailField,
            'password1': forms.fields.CharField,
            'password2': forms.fields.CharField,
        }
        response = self.authorized_client.get(reverse('users:signup'))
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_password_reset_form_show_correct_context(self):
        """Шаблон password_reset_form сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('users:password_reset_form')
        )
        form_field = response.context.get('form').fields.get('email')
        self.assertIsInstance(form_field, forms.fields.EmailField)
