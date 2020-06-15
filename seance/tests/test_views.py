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


class AuthenticationTestCase(TestCase, BaseInitial):

    def setUp(self):
        BaseInitial.__init__(self)

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
        invalid_username = {'username': self.admin.username, 'password1': 'password4321',
                            'password2': 'password4321'}
        response = self.client.post('/accounts/register/', data=invalid_username)
        page = response.content.decode()
        self.assertInHTML('<li>A user with that username already exists.</li>', page)

        common_password = {'username': 'user1', 'password1': 'pass1234',
                            'password2': 'pass1234'}
        response = self.client.post('/accounts/register/', data=common_password)
        page = response.content.decode()
        self.assertInHTML('<li>This password is too common.</li>', page)

        short_password = {'username': 'user1', 'password1': 'pass',
                            'password2': 'pass'}
        response = self.client.post('/accounts/register/', data=short_password)
        page = response.content.decode()
        self.assertInHTML('<li>Ensure this value has at least 8 characters (it has 4).</li>', page)

        password_mismatch = {'username': 'user1', 'password1': 'pass9513',
                             'password2': 'pass9531'}
        response = self.client.post('/accounts/register/', data=password_mismatch)
        page = response.content.decode()
        self.assertInHTML('<li>passwords mismatch</li>', page)

        password2_not_set = {'username': 'user1', 'password1': 'pass9513',
                             'password2': ''}
        response = self.client.post('/accounts/register/', data=password2_not_set)
        page = response.content.decode()
        self.assertInHTML('<li>This field is required.</li>', page)

        username_short = {'username': 'u1', 'password1': 'pass9513',
                          'password2': 'pass9513'}
        response = self.client.post('/accounts/register/', data=username_short)
        page = response.content.decode()
        # post was't sent by browser because username too short
        self.assertFalse(page)

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



