from django.utils.deprecation import MiddlewareMixin

from cinema import settings


class LogoutIfNotActiveMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'user'), (
            'The LogoutIfNotActiveMiddleware middleware requires authentication middleware to be installed.'
        )
        if request.user.is_authenticated:
            pass


        request.user = SimpleLazyObject(lambda: get_user(request))
