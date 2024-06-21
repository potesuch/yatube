from django.shortcuts import render


def page_not_found(request, exception):
    """
    Представление для отображения страницы ошибки 404 (Страница не найдена).
    """
    return render(request, 'core/404.html', {'path': request.path}, status=404)


def page_permission_denied(request, exception):
    """
    Представление для отображения страницы ошибки 403 (Доступ запрещен).
    """
    return render(request, 'core/403.html', status=403)


def page_server_error(request):
    """
    Представление для отображения страницы ошибки 500 (Внутренняя ошибка сервера).
    """
    return render(request, 'core/500.html', status=500)


def csrf_failure(request, reason=''):
    """
    Представление для отображения страницы ошибки CSRF (Недопустимая CSRF токен).
    """
    return render(request, 'core/403csrf.html')
