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
