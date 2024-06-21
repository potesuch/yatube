from django.views.generic import TemplateView


class AboutAuthorView(TemplateView):
    """
    Представление для отображения страницы "Об авторе".

    Использует шаблон 'about/author.html'.
    """
    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    """
    Представление для отображения страницы "Технологии".

    Использует шаблон 'about/tech.html'.
    """
    template_name = 'about/tech.html'
