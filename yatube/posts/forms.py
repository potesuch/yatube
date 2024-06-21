from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """
    Форма для создания и редактирования постов.

    Использует модель Post и включает поля text, group и image.
    """

    class Meta:
        model = Post
        fields = ('text', 'group', 'image')


class CommentForm(forms.ModelForm):
    """
    Форма для создания комментариев.

    Использует модель Comment и включает поле text.
    """

    class Meta:
        model = Comment
        fields = ('text',)
