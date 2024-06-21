from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class CustomPagination(LimitOffsetPagination):
    """
    Класс для кастомной пагинации.

    Возвращает ответ с полем 'count' (общее количество объектов) и
    'response' (список объектов текущей страницы).
    """

    def get_paginated_response(self, data):
        return Response({
            'count': self.count,
            'response': data
        })
