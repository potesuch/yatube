from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Post, Group, User, Comment, Tag, TagPost, Follow


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Tag.

    Поле 'tag_name' отображает название тега.
    """
    tag_name = serializers.CharField(source='name')

    class Meta:
        model = Tag
        fields = ('tag_name',)


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Post.

    Включает дополнительные поля для автора, группы, комментариев и тегов.
    """
    author = serializers.SerializerMethodField()
    group = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Group.objects.all(),
                                         required=False)
    comments = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, required=False)
    publication_date = serializers.DateTimeField(source='pub_date',
                                                 read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'group', 'tags',
                  'comments', 'publication_date')

    def create(self, validated_data):
        """
        Создает новый объект Post, учитывая теги, если они есть.
        """
        if 'tags' not in self.initial_data:
            post = Post.objects.create(**validated_data)
            return post
        tags = validated_data.pop('tags')
        post = Post.objects.create(**validated_data)
        for tag in tags:
            current_tag, _ = Tag.objects.get_or_create(**tag)
            TagPost.objects.create(tag=current_tag, post=post)
            return post

    def update(self, instance, validated_data):
        """
        Обновляет существующий объект Post, включая обновление тегов.
        """
        if 'tags' not in self.initial_data:
            return super().update(instance, validated_data)
        tags = validated_data.pop('tags')
        instance_tags = TagPost.objects.filter(post=instance)
        for tag in tags:
            current_tag, _ = Tag.objects.get_or_create(**tag)
            if current_tag not in instance_tags:
                TagPost.objects.create(tag=current_tag, post=instance)
        for tag in instance_tags:
            if tag not in tags:
                tag.delete()
        super().update(instance, validated_data)
        return instance

    def get_author(self, obj):
        """
        Получает имя пользователя автора поста.
        """
        return obj.author.username

    def get_comments(self, obj):
        """
        Получает количество комментариев к посту.
        """
        return obj.comments.count()


class PostListSerializer(PostSerializer):
    """
    Сериализатор для списка постов.

    Включает основные поля поста.
    """

    class Meta:
        model = Post
        fields = ('id', 'author', 'text', 'comments', 'group', 'pub_date')


class GroupSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Group.

    Включает основные поля группы.
    """

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.

    Включает поля для поста, автора, текста и даты создания комментария.
    """
    author = serializers.PrimaryKeyRelatedField(
        source='author.username', read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'text', 'created')
        read_only_fields = ('post', 'created')


class FollowSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Follow.

    Включает поля для пользователя и его подписок.
    """
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('id', 'user', 'following',)
        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            ),
        )

    def validate_following(self, value):
        """
        Валидатор для проверки, что пользователь не подписывается сам на себя.
        """
        user = self.context['request'].user
        if user == value:
            raise serializers.ValidationError
        return value
