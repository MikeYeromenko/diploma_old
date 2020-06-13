from django.test import TestCase

from seance.tests.test_models import BaseInitial


class SeanceListViewTestCase(TestCase, BaseInitial):

    def setUp(self):
        BaseInitial.__init__(self)

    def test_basic(self):
        """
        Tests that SeanceListView returns a 200 response, uses correct template and has correct context
        """
        with self.assertTemplateUsed('seance/index.html'):
            response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # import pdb; pdb.set_trace()

        self.assertEqual(len(response.context['seance_list']), 1)

        self.assertEqual(response.context['seance_list'][0].film.title, 'James Bond')

