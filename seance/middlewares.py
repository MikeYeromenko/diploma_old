from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from cinema import settings
from seance.models import AdvUser


class LogoutIfInActiveMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'user'), (
            'The LogoutIfNotActiveMiddleware middleware requires authentication middleware to be installed.'
        )
        if request.user.is_authenticated:
            if request.user.last_activity > timezone.now() - timezone.timedelta(minutes=5):
                user = get_object_or_404(AdvUser, pk=request.user.pk)
                user.last_activity = timezone.now()
                user.save()
                request.user.last_activity = user.last_activity
            else:
                logout(request)

