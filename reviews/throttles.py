from rest_framework.throttling import SimpleRateThrottle


class ReviewRateThrottle(SimpleRateThrottle):
    scope = 'review'

    def get_cache_key(self, request, view):
        if not request.user.is_authenticated:
            return None
        return f'review_throttle_{request.user.id}'

    def parse_rate(self, rate):
        # 10 soniyada 1 ta so'rov
        return (1, 10)