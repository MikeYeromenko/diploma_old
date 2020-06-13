from django.test import TestCase


class SeanceViewsBaseTestCase(TestCase):

    def setUp(self):
        pass


class SeanceListViewTestCase(SeanceViewsBaseTestCase):

    def test_basic(self):
        """
        Tests that SeanceListView returns a 200 response, uses correct template and has correct context
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed('seance/index.html'):
            self.assertEqual(len(response.context['seances']), 2)

