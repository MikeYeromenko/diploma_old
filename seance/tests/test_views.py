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


class AuthenticationTestCase(TestCase):

    def test_basic_registration(self):
        """
        Tests that RegisterUserView returns a 200 response, uses correct template
        """
        with self.assertTemplateUsed('registration/register_user.html'):
            response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)

    def test_registration(self):
        """
        Test RegistrationUserView deeply, with different types of errors
        """
        invalid_username = {'username': 'admin', 'password1': 'password4321', 'password2': 'password4321'}
        response = self.client.post('/accounts/register/', data=invalid_username)
        page = response.content.decode()
        import pdb; pdb.set_trace()
        self.assertInHTML('This name already exists', page)

    def test_basic_login(self):
        """
        Tests that UserLoginView returns a 200 response, uses correct template
        """
        with self.assertTemplateUsed('registration/login.html'):
            response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_user_detail_view(self):
        """
        Tests that UserDetailView returns a 200 response, uses correct template
        """
        with self.assertTemplateUsed('seance/profile.html'):
            response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)



