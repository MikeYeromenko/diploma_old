from django.test import TestCase
from django.urls import reverse_lazy

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

    def test_deep_SeanceListView(self):
        """
        Test that SeanceListView renders template with data we expected
        """
        response = self.client.get(reverse_lazy('seance:index'))
        page = response.content.decode()
        import pdb; pdb.set_trace()


class AuthenticationTestCase(TestCase, BaseInitial):

    def setUp(self):
        BaseInitial.__init__(self)

    def test_basic_registration(self):
        """
        Tests that RegisterUserView returns a 200 response, uses correct template
        """
        with self.assertTemplateUsed('registration/register_user.html'):
            response = self.client.get(reverse_lazy('seance:register'))
        self.assertEqual(response.status_code, 200)

    def test_deep_registration(self):
        """
        Test RegistrationUserView deeply, with different types of errors
        """
        # username exists
        existed_username = {'username': self.admin.username, 'password1': 'password4321',
                            'password2': 'password4321'}
        response = self.client.post(reverse_lazy('seance:register'), data=existed_username)
        page = response.content.decode()
        self.assertInHTML('<li>A user with that username already exists.</li>', page)

        # common password
        common_password = {'username': 'user1', 'password1': 'pass1234',
                           'password2': 'pass1234'}
        response = self.client.post(reverse_lazy('seance:register'), data=common_password)
        page = response.content.decode()
        self.assertInHTML('<li>This password is too common.</li>', page)

        # password has less than 8 symbols
        short_password = {'username': 'user1', 'password1': 'pass',
                          'password2': 'pass'}
        response = self.client.post(reverse_lazy('seance:register'), data=short_password)
        page = response.content.decode()
        self.assertInHTML('<li>Ensure this value has at least 8 characters (it has 4).</li>', page)

        # password1 and password2 mismatch
        password_mismatch = {'username': 'user1', 'password1': 'pass9513',
                             'password2': 'pass9531'}
        response = self.client.post(reverse_lazy('seance:register'), data=password_mismatch)
        page = response.content.decode()
        self.assertInHTML('<li>passwords mismatch</li>', page)

        # password2 didn't fill in
        password2_not_set = {'username': 'user1', 'password1': 'pass9513',
                             'password2': ''}
        response = self.client.post(reverse_lazy('seance:register'), data=password2_not_set)
        page = response.content.decode()
        self.assertInHTML('<li>This field is required.</li>', page)

        # username short
        username_short = {'username': 'u1', 'password1': 'pass9513',
                          'password2': 'pass9513'}
        response = self.client.post(reverse_lazy('seance:register'), data=username_short)
        page = response.content.decode()
        # post was't sent by browser because username too short
        self.assertFalse(page)

    def test_deep_login(self):
        """
        Tests UserLoginView deeply, with different kinds of errors
        """
        # after successful login user is redirected
        correct_data = {'username': self.admin.username, 'password': 'password1'}
        response = self.client.post(reverse_lazy('seance:login'), data=correct_data)
        self.assertRedirects(response, reverse_lazy('seance:profile'))

        # login with correct data when user is already logged in
        correct_data = {'username': self.admin.username, 'password': 'password1'}
        response = self.client.post(reverse_lazy('seance:login'), data=correct_data)
        page = response.content.decode()
        # post was't sent by browser because user with that credentials is logged in
        self.assertFalse(page)

        self.client.get(reverse_lazy('seance:logout'))

        incorrect_username = {'username': 'wrong', 'password': 'password1'}
        response = self.client.post('/accounts/login/', data=incorrect_username)
        page = response.content.decode()
        self.assertInHTML('<li>Please enter a correct username and password. '
                          'Note that both fields may be case-sensitive.</li>', page)

        incorrect_password = {'username': 'admin', 'password': 'wrong'}
        response = self.client.post(reverse_lazy('seance:login'), data=incorrect_password)
        page = response.content.decode()
        self.assertInHTML('<li>Please enter a correct username and password. '
                          'Note that both fields may be case-sensitive.</li>', page)

        empty_data = {'username': '', 'password': ''}
        response = self.client.post(reverse_lazy('seance:login'), data=empty_data)
        page = response.content.decode()
        self.assertInHTML('<li>This field is required.</li>', page)

    def test_user_detail_view(self):
        """
        Tests that UserDetailView returns a 200 response, uses correct template
        """
        with self.assertTemplateUsed('seance/profile.html'):
            response = self.client.get(reverse_lazy('seance:profile'))
        self.assertEqual(response.status_code, 200)

    def test_basic_login_logout(self):
        """
        Tests that UserLoginView and UserLogoutView returns a 200 response, uses correct template
        After user logged in he is able to logout
        """
        # login
        with self.assertTemplateUsed('registration/login.html'):
            response = self.client.get(reverse_lazy('seance:login'))
        self.assertEqual(response.status_code, 200)

        # logout
        with self.assertTemplateUsed('registration/logged_out.html'):
            response = self.client.get(reverse_lazy('seance:logout'))
        self.assertEqual(response.status_code, 200)
        page = response.content.decode()
        self.assertInHTML('<p>You have logged out successfully</p>', page)




