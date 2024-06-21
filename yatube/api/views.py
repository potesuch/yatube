from rest_framework import viewsets
from rest_framework import filters
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import exceptions

from posts.models import Post, Group, Comment, Follow
from .serializers import (PostSerializer, PostListSerializer, GroupSerializer,
                          CommentSerializer, FollowSerializer,)
from .permissions import IsAuthorOrReadOnly
# from .throttling import LunchBreakThrottle
# from .pagination import CustomPagination


class PostViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работы с постами.

    Поддерживает все CRUD операции и включает фильтрацию по тексту и сортировку по дате публикации.
    """
    queryset = Post.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    # throttle_classes = (LunchBreakThrottle,)
    # pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('$text',)
    ordering_fields = ('pub_date',)

    def get_serializer_class(self):
        """
        Возвращает сериализатор в зависимости от действия (list или другие).
        """
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        """
        Устанавливает текущего пользователя как автора поста при его создании.
        """
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для работы с группами.

    Поддерживает только чтение.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthorOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работы с комментариями.

    Поддерживает все CRUD операции.
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        """
        Возвращает комментарии к конкретному посту.
        """
        post_id = self.kwargs.get('post_id')
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise exceptions.NotFound
        queryset = Comment.objects.filter(post=post)
        return queryset

    def perform_create(self, serializer):
        """
        Устанавливает текущего пользователя как автора комментария и связывает его с постом.
        """
        post_id = self.kwargs.get('post_id')
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise exceptions.NotFound
        serializer.save(post=post, author=self.request.user)


class FollowViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    Вьюсет для работы с подписками.

    Поддерживает получение списка, создание и удаление подписок.
    """
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """
        Возвращает список подписок текущего пользователя.
        """
        queryset = Follow.objects.all()
        user = self.request.user
        queryset = queryset.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        """
        Устанавливает текущего пользователя как подписчика.
        """
        serializer.save(user=self.request.user)
