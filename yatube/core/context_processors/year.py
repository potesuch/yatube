from datetime import date


def year(request):
    """
    Контекстный процессор, добавляющий текущий год в контекст шаблона.

    Возвращает словарь с текущим годом под ключом 'year'.
    """
    return {
        'year': date.today().year,
    }
