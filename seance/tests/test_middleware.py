from django.test import TestCase
from django.urls import reverse_lazy
from django.utils import timezone

from seance.models import AdvUser


class CustomMiddlewareTestCase(TestCase):

    def setUp(self):
        self.user = AdvUser.objects.create(
            username='user1',
            email='user1@somesite.com',
            first_name='Mike',
            last_name='Yeromenko',
            wallet=10000
        )
        self.user.set_password('password1')
        self.user.save()

        self.user_old = AdvUser.objects.create(
            username='user2',
            email='user1@somesite.com',
            first_name='Mike',
            last_name='Yeromenko',
            wallet=10000,
        )
        self.user_old.set_password('password2')
        self.user_old.last_activity = timezone.now() - timezone.timedelta(days=1)
        self.user_old.save()

    def test_LogoutIfInActiveMiddleware(self):
        """
        Tests that custom middleware logs out user if he is more then 5 minutes inactive
        """

        # login user with last activity set to timezone.now()
        auth_data = {'username': self.user.username, 'password': 'password1'}
        response = self.client.post('/accounts/login/', data=auth_data)
        self.assertRedirects(response, reverse_lazy('seance:profile'))

        # we have authenticated user and go with him to index page
        response = self.client.get(reverse_lazy('seance:index'))
        self.assertTrue(response.context.get('user').is_authenticated)

        # set user's last activity to -5 minutes
        self.user.last_activity = timezone.now() - timezone.timedelta(minutes=5)
        self.user.save()

        # user is authenticated with last activity more than 5 minutes age.
        # LogoutIfInActiveMiddleware logged him out with message 'More than 5 minutes....'
        response = self.client.get(reverse_lazy('seance:index'))
        self.assertFalse(response.context.get('user').is_authenticated)
        page = response.content.decode()
        self.assertInHTML('<p>More than 5 minutes inactive. Please login again</p>', page)

        # login user with last_activity 5 days ago set to timezone.now() - timezone.timedelta(days=5)

        auth_data = {'username': self.user_old.username, 'password': 'password2'}
        response = self.client.post('/accounts/login/', data=auth_data)
        self.assertRedirects(response, reverse_lazy('seance:profile'))

        # when user logs in, user.last_activity field updates to timezone_now()

        response = self.client.get(reverse_lazy('seance:index'))
        self.assertTrue(response.context.get('user').is_authenticated)

