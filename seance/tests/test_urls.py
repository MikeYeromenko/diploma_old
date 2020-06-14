from unittest.case import TestCase

from django.urls import resolve


class CinemaUrlsTestCase(TestCase):

    def test_root_url_uses_seance_list_view(self):
        """
        Tests that the root of the site resolves to the correct class-based View, and url has correct name
        """
        root = resolve('/')
        self.assertEqual(root.func.__name__, 'SeanceListView')
        self.assertEqual(root.url_name, 'index')
        
    def test_url_for_registration(self):
        """
        Test that url accounts/register/ exists, resolves to the correct cbv and has expected name
        """
        registration = resolve('/accounts/register/')
        self.assertEqual(registration.func.__name__, 'RegisterUserView')
        self.assertEqual(registration.url_name, 'register')
