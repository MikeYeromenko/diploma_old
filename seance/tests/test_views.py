import datetime

from django.db.models import Q
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils import timezone

from seance.models import Seance, Hall
from seance.tests.test_models import BaseInitial


class SeanceListViewTestCase(TestCase, BaseInitial):

    def setUp(self):
        BaseInitial.__init__(self)
        self.create_seance_objects_for_tests()

    def create_seance_objects_for_tests(self):
        Seance.objects.create(
            film=self.film,
            date_starts=datetime.date.today(),
            date_ends=datetime.date.today() + datetime.timedelta(days=15),
            time_starts=datetime.time(18),
            hall=self.hall,
            is_active=True,
            description='Some text',
            ticket_price=150,
            admin=self.admin,
        )

        Seance.objects.create(
            film=self.film,
            date_starts=datetime.date.today(),
            date_ends=datetime.date.today() + datetime.timedelta(days=15),
            time_starts=datetime.time(18),
            hall=self.hall,
            is_active=False,
            description='Some text',
            ticket_price=150,
            admin=self.admin,
        )

        Seance.objects.create(
            film=self.film,
            date_starts=datetime.date.today() + datetime.timedelta(days=15),
            date_ends=datetime.date.today() + datetime.timedelta(days=30),
            time_starts=datetime.time(18),
            hall=self.hall,
            is_active=True,
            description='Some text',
            ticket_price=140,
            admin=self.admin,
        )

        hall2 = Hall.objects.create(
            name='Green',
            rows=15,
            seats=20,
            is_active=True,
            description='Some text about why this hall is the best',
            admin=self.admin
        )

        Seance.objects.create(
            film=self.film,
            date_starts=datetime.date.today(),
            date_ends=datetime.date.today() + datetime.timedelta(days=15),
            time_starts=datetime.time(17),
            hall=hall2,
            is_active=True,
            description='Some text',
            ticket_price=200,
            admin=self.admin,
        )

    def test_basic(self):
        """
        Tests that SeanceListView returns a 200 response, uses correct template and has correct context
        """
        with self.assertTemplateUsed('seance/index.html'):
            response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        quantity = Seance.objects.filter(Q(date_starts__lte=datetime.date.today()) & Q(date_ends__gte=datetime.date.today()) &
                                         Q(time_starts__gt=timezone.now()) & Q(is_active=True)).count()

        self.assertEqual(len(response.context['seance_list']), quantity)

        self.assertEqual(response.context['seance_list'][0].film.title, 'James Bond')

    # def test_deep_SeanceListView(self):
    #     """
    #     Test that SeanceListView renders template with data we expected
    #     """
    #     # There are seances: 12:00 today, 18:00 today, 18:00 today not active, 18:00 today+15days, 17:00 today
    #     response = self.client.get(reverse_lazy('seance:index'))
    #     self.assertEqual(len(response.context.get('seance_list')), 3)

    def test_ordering_queryset(self):
        """
        Test ordering_queryset method
        """
        # test ordering 'from expensive to cheap'
        response = self.client.get(reverse_lazy('seance:index'), data={'ordering': 'expensive'})
        seances = response.context.get('seance_list')

        seances_test = Seance.objects.filter(
            Q(date_starts__lte=datetime.date.today()) & Q(date_ends__gte=datetime.date.today()) &
            Q(time_starts__gt=timezone.now()) & Q(is_active=True)).order_by('-ticket_price')

        # the quantity of elements in seances dependes upon a time of the day. In the evening there may be
        # a situation, that seances is empty, because time_starts of them passed
        if seances_test:
            self.assertEqual(seances[0].ticket_price, seances_test[0].ticket_price)
            if len(seances_test) > 2:
                self.assertEqual(seances[1].ticket_price, seances_test[1].ticket_price)

        # test ordering 'latest'
        response = self.client.get(reverse_lazy('seance:index'), data={'ordering': 'latest'})
        seances = response.context.get('seance_list')

        seances_test = Seance.objects.filter(
            Q(date_starts__lte=datetime.date.today()) & Q(date_ends__gte=datetime.date.today()) &
            Q(time_starts__gt=timezone.now()) & Q(is_active=True)).order_by('-time_starts')
        if seances_test:
            self.assertEqual(seances[0].time_starts, seances_test[0].time_starts)
            if len(seances_test) > 2:
                self.assertEqual(seances[1].time_starts, seances_test[1].time_starts)

        # test ordering 'closest'
        response = self.client.get(reverse_lazy('seance:index'), data={'ordering': 'closest'})
        seances = response.context.get('seance_list')

        seances_test = Seance.objects.filter(
            Q(date_starts__lte=datetime.date.today()) & Q(date_ends__gte=datetime.date.today()) &
            Q(time_starts__gt=timezone.now()) & Q(is_active=True)).order_by('time_starts')
        if seances_test:
            self.assertEqual(seances[0].time_starts, seances_test[0].time_starts)
            if len(seances_test) > 2:
                self.assertEqual(seances[1].time_starts, seances_test[1].time_starts)

    def test_tomorrow_option(self):
        """
        Tests that Seances for tomorrow will be gotten correctly
        """
        # for this create seance, ending today, so tomorrow it will not be in queryset
        Seance.objects.create(
            film=self.film,
            date_starts=datetime.date.today() - datetime.timedelta(days=5),
            date_ends=datetime.date.today(),
            time_starts=datetime.time(22),
            hall=self.hall,
            is_active=True,
            description='Some text',
            ticket_price=200,
            admin=self.admin,
        )
        response = self.client.get(reverse_lazy('seance:index'))
        seances = response.context.get('seance_list')
        quantity = Seance.objects.filter(Q(date_starts__lte=datetime.date.today()) & Q(date_ends__gte=datetime.date.today()) &
                                         Q(time_starts__gt=timezone.now()) & Q(is_active=True)).count()
        self.assertEqual(len(seances), quantity)

        # but tomorrow it has to show 3 seances

        response = self.client.get(reverse_lazy('seance:index'), data={'days': 'tomorrow'})
        seances = response.context.get('seance_list')
        self.assertEqual(len(seances), 3)

        # lets add new seance beginning from tomorrow
        # Total quantity of seances for today will be 'quantity', and for tomorrow - 4

        Seance.objects.create(
            film=self.film,
            date_starts=datetime.date.today() + datetime.timedelta(days=1),
            date_ends=datetime.date.today() + datetime.timedelta(days=5),
            time_starts=datetime.time(22),
            hall=self.hall,
            is_active=True,
            description='Some text',
            ticket_price=200,
            admin=self.admin,
        )

        response = self.client.get(reverse_lazy('seance:index'), data={'days': 'tomorrow'})
        seances = response.context.get('seance_list')
        # import pdb; pdb.set_trace()
        self.assertEqual(len(seances), 4)

        # but for today it will not change
        response = self.client.get(reverse_lazy('seance:index'))
        seances = response.context.get('seance_list')
        self.assertEqual(len(seances), quantity)


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


class BasketViewTestCase(TestCase, BaseInitial):

    def setUp(self):
        BaseInitial.__init__(self)

    def test_basket_view(self):
        """
        Test that basket view works correctly
        """
        with self.assertTemplateUsed('seance/basket.html'):
            response = self.client.get(reverse_lazy('seance:basket'))
        self.assertEqual(response.status_code, 200)


class SeanceDeatailViewTestCase(TestCase, BaseInitial):

    def setUp(self):
        BaseInitial.__init__(self)

    def test_basic(self):
        """
        Test that basket view works correctly
        """
        with self.assertTemplateUsed('seance/seance_detail.html'):
            response = self.client.get(reverse_lazy('seance:seance_detail', kwargs={'pk': self.seance.pk}))
        self.assertEqual(response.status_code, 200)
