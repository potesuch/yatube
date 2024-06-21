import datetime
from rest_framework.throttling import BaseThrottle

class WorkingHoursRateThrottle(BaseThrottle):

    def allow_request(self, request, view):
        now = datetime.datetime.now().hour
        if 3 <= now <= 5:
            return False
        return True
