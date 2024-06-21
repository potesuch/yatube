from django.views.generic.edit import CreateView
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from .forms import CreationForm, ResetForm


class SignUp(CreateView):
    """
    Представление для регистрации нового пользователя.

    Использует форму CreationForm для создания нового пользователя.
    После успешной регистрации перенаправляет на главную страницу.
    """
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class PasswordReset(PasswordResetView):
    """
    Представление для сброса пароля.

    Использует форму ResetForm для сброса пароля. После успешной отправки
    формы перенаправляет на страницу подтверждения сброса пароля.
    """
    form_class = ResetForm
    success_url = reverse_lazy('users:password_reset_done')
    template_name = 'users/password_reset_form.html'
