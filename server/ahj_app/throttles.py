from rest_framework.throttling import UserRateThrottle
from django.conf import settings

class MemberRateThrottle(UserRateThrottle):
    # Define a custom scope name to be referenced by DRF in settings.py
    scope = "member"

    def __init__(self):
        super().__init__()

    def allow_request(self, request, view):
        """
        Override rest_framework.throttling.SimpleRateThrottle.allow_request

        Check to see if the request should be throttled.

        On success calls `throttle_success`.
        On failure calls `throttle_failure`.
        """
        if request.user.is_staff:
            # No throttling
            return True

        if not request.user.is_authenticated:
            # Unauthenticated user will be blocked by authentication guard
            # Returning False will give the user a throttle error instead of an authentication error
            return True

        self.key = f'User{request.user.pk}'
        # Original logic from the parent method (besides cache key determination)
        if self.rate is None or self.key is None:
            return True
        self.history = self.cache.get(self.key, [])
        self.now = self.timer()

        # Drop any requests from the history which have now passed the
        # throttle duration
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()
        if len(self.history) >= self.num_requests:
            return self.throttle_failure()
        return self.throttle_success()

    def parse_rate(self, rate):
        """
        Given the request rate string, return a two tuple of:
        <allowed number of requests>, <period of time in seconds>
        """
        if rate is None:
            return (None, None)
        num, period = rate.split('/')
        num_requests = int(num)
        if (period == 'month'): # Period is 30 days
            duration = 2592000
        else:
            duration = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[period[0]]
        return (num_requests, duration)

class WebpageSearchThrottle(UserRateThrottle):
    # Define a custom scope name to be referenced by DRF in settings.py
    scope = "webpage-search"

    def allow_request(self, request, view):
        """
        Implement the check to see if the request should be throttled.
        On success calls `throttle_success`.
        On failure calls `throttle_failure`.
        """
        if self.user_is_member(request.user) or request.user.is_staff:
            return True
        if self.rate is None:
            return True

        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        self.history = self.cache.get(self.key, [])
        self.now = self.timer()
        # Drop any requests from the history which have now passed the
        # throttle duration
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()
        if len(self.history) >= self.num_requests:
            return self.throttle_failure()
        return self.throttle_success()
    
    def user_is_member(self, user):
        if user.is_authenticated:
            if user.MemberID or user.get_API_token(): # Allows access if member OR if they have an API token
                return True                         
        return False                                