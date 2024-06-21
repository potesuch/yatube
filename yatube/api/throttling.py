from django.utils import timezone
from rest_framework.throttling import BaseThrottle


class LunchBreakThrottle(BaseThrottle):
    """
    Класс для ограничения запросов во время обеденного перерыва (с 13 до 14 часов).
    """

    def allow_request(self, request, view):
        now = timezone.now().hour
        if 13 <= now <= 14:
            return False
        return True
