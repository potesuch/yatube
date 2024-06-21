from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Post, Group, User, Comment, Follow
from .forms import PostForm, CommentForm


def index(request):
    """
    Представление для главной страницы сайта.

    Отображает список всех постов, поддерживает поиск по ключевому слову.
    """
    template = 'posts/index.html'
    keyword = request.GET.get('q', None)
    page_number = request.GET.get('page', None)
    if keyword:
        posts = (Post.objects.filter(text__contains=keyword)
                 .select_related('author')
                 .select_related('group'))
    else:
        posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'keyword': keyword,
    }
    return render(request, template, context)


def group_posts(request, slug):
    """
    Представление для отображения постов определенной группы.

    Отображает список постов, принадлежащих группе с указанным slug.
    """
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    page_number = request.GET.get('page')
    posts = Post.objects.filter(group=group)
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'group': group,
    }
    return render(request, template, context)


def profile(request, username):
    """
    Представление для отображения профиля пользователя.

    Отображает список постов, созданных пользователем с указанным username.
    """
    template_name = 'posts/profile.html'
    user = request.user
    author = get_object_or_404(User, username=username)
    if user.is_authenticated and user != author:
        following = Follow.objects.filter(
            user=request.user,
            following=author
        ).exists()
    else:
        following = None
    posts = author.posts.all()
    page = request.GET.get('page')
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page)
    context = {
        'author': author,
        'following': following,
        'page_obj': page_obj
    }
    return render(request, template_name, context)


def post_detail(request, post_id):
    """
    Представление для отображения деталей поста.

    Отображает полный текст поста и комментарии к нему.
    """
    template_name = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm()
    comments = Comment.objects.filter(post=post)
    paginator = Paginator(comments, 10)
    page_obj = paginator.get_page(request.GET)
    context = {
        'post': post,
        'form': form,
        'page_obj': page_obj,
    }
    return render(request, template_name, context)


@login_required
def post_create(request):
    """
    Представление для создания нового поста.

    Доступно только для авторизованных пользователей.
    """
    template_name = 'posts/post_form.html'
    form = PostForm(
        request.POST or None,
        files=request.FILES
    )
    context = {
        'form': form,
        'is_edit': False
    }
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', post.author.username)
    return render(request, template_name, context)


@login_required
def post_edit(request, post_id):
    """
    Представление для редактирования существующего поста.

    Доступно только для авторизованных пользователей и авторов поста.
    """
    template_name = 'posts/post_form.html'
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        return redirect('posts:post_detail', post_id=post.id)
    context = {
        'form': form,
        'post': post,
        'is_edit': True
    }
    return render(request, template_name, context)


@login_required
def add_comment(request, post_id):
    """
    Представление для добавления комментария к посту.

    Доступно только для авторизованных пользователей.
    """
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    """
    Представление для отображения постов авторов, на которых подписан пользователь.

    Доступно только для авторизованных пользователей.
    """
    template_name = 'posts/follow.html'
    posts = Post.objects.filter(author__following__user=request.user)
    page_number = request.GET.get('page')
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template_name, context)


@login_required
def profile_follow(request, username):
    """
    Представление для подписки на пользователя.

    Доступно только для авторизованных пользователей.
    """
    user = request.user
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(
        user=request.user,
        following=author
    )
    following = follow.exists()
    if user != author and not following:
        follow = Follow.objects.create(
            user=request.user,
            following=author
        )
        follow.save()
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    """
    Представление для отписки от пользователя.

    Доступно только для авторизованных пользователей.
    """
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(
        user=request.user,
        following=author
    )
    following = follow.exists()
    if following:
        follow.delete()
    return redirect('posts:profile', username=username)


@login_required
def post_delete(request, post_id):
    """
    Представление для удаления поста.

    Доступно только для авторизованных пользователей и авторов поста.
    """
    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:
        post.delete()
    return redirect('posts:index')
