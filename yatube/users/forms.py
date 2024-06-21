from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CreationForm(UserCreationForm):
    """
    Форма для создания нового пользователя.

    Поля формы включают имя пользователя и электронную почту.
    """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email',)


class ResetForm(PasswordResetForm):
    """
    Форма для сброса пароля пользователя.

    Добавляет валидацию для поля электронной почты.
    """

    def clean_email(self):
        """
        Проверка наличия электронной почты в базе данных.

        Возвращает ошибку, если указанный email не найден среди пользователей.
        """
        email = self.cleaned_data['email']
        email_exists = User.objects.filter(email=email)
        if not email_exists:
            self.add_error('email', 'Такой email не найден')
        return email
