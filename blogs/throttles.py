from rest_framework.throttling import SimpleRateThrottle
from rest_framework.exceptions import Throttled


class IPRateThrottle(SimpleRateThrottle):
    rate = '10/day'
    
    def get_cache_key(self, request, view):
        ip_addr = self.get_ident(request)
        return f'ip:{ip_addr}'
    
    def throttle_failure(self):
        raise Throttled(detail={})