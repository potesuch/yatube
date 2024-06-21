from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
    """
    Модель для тегов.

    Содержит поле name для хранения названия тега.
    """
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Group(models.Model):
    """
    Модель для групп постов.

    Содержит поля title, slug и description.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return f'Группа: {self.title} - {self.description}'

    def get_absolute_url(self):
        """
        Возвращает абсолютный URL для группы.
        """
        return reverse('posts:group_list', args=[self.slug])


class Post(models.Model):
    """
    Модель для постов.

    Содержит поля text, pub_date, author, group, image и tags.
    """
    text = models.TextField(
        'Текст поста',
        help_text='Введите текст поста'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Группа',
        help_text='Выберите группу'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )
    tags = models.ManyToManyField(Tag, through='TagPost')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """
    Модель для комментариев к постам.

    Содержит поля post, author, text и created.
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата комментария',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Follow(models.Model):
    """
    Модель для подписок на авторов.

    Содержит поля user и following, которые ссылаются на модель User.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    def __str__(self):
        return (f'{self.user}: {self.following}')


class TagPost(models.Model):
    """
    Промежуточная модель для связи тегов и постов.

    Содержит поля tag и post, которые ссылаются на соответствующие модели.
    """
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag}: {self.post}'


class Contact(models.Model):
    """
    Модель для хранения контактной информации.

    Содержит поля name, email, subject, body и is_answered.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    body = models.TextField()
    is_answered = models.BooleanField(default=False)
