import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from seance.models import Film, Hall, Seance


class SeanceInitial(TestCase):

    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username='admin', email='admin@somesite.com'
        )
        self.admin.set_password('password1')
        self.admin.save()
        self.film = Film.objects.create(
            title='James Bond',
            starring='Daniel Craig and co',
            director='Director',
            duration=datetime.time(1, 40),
            description='some text....',
            admin=self.admin,
            is_active=True,
        )

        self.hall = Hall.objects.create(
            name='Yellow',
            size=50,
            is_active=True,
            description='Some text about why this hall is the best',
            admin=self.admin
        )

        self.seance = Seance.objects.create(
            film=self.film,
            date_starts=datetime.date.today(),
            date_ends=datetime.date.today() + datetime.timedelta(days=15),
            time_starts=datetime.time(12),
            places_taken=0,
            hall=self.hall,
            is_active=True,
            description='Some text about why this seance is the best',
            ticket_price=100,
            admin=self.admin,
        )


class SeanceModelsTestCase(SeanceInitial):

    def test_film_model_basic(self):
        """
        Tests that Film object was created correctly
        """
        self.assertEqual(self.film.title, 'James Bond')
        self.assertEqual(self.film.duration, datetime.time(1, 40))

    def test_hall_model_basic(self):
        """
        Tests that Hall object was created correctly
        """
        self.assertEqual(self.hall.name, 'Yellow')
        self.assertEqual(self.hall.size, 50)

    def test_seance_model_basic(self):
        """
        Tests that Seance object was created correctly
        """
        self.assertEqual(self.seance.film.title, 'James Bond')
        self.assertEqual(self.seance.ticket_price, 100)
        self.assertEqual(self.seance.time_ends, datetime.time(13, 50))

    def test_default_seance_end_date_auto_added(self):
        """
        Test if admin didn't set end of seance the default value will be added (start time + 15 days)
        """
        seance = Seance.objects.create(
            film=self.film,
            date_starts=datetime.date.today(),
            time_starts=datetime.time(14),
            time_ends=datetime.time(16),
            places_taken=0,
            hall=self.hall,
            is_active=True,
            description='Some text about why this seance is the best',
            ticket_price=100,
            admin=self.admin,
        )
        self.assertEqual(seance.date_ends, seance.date_starts + datetime.timedelta(days=15))

    def test_seance_set_time_ends(self):
        """
        Test the seance time_ends to be set correctly
        """
        seance = Seance.objects.create(
            film=self.film,
            date_starts=datetime.date.today(),
            date_ends=datetime.date.today() + datetime.timedelta(days=30),
            time_starts=datetime.time(23),
            places_taken=0,
            hall=self.hall,
            is_active=True,
            description='Some text about why this seance is the best',
            ticket_price=100,
            admin=self.admin,
        )
        self.assertEqual(seance.time_ends, datetime.time(0, 50))

        seance2 = Seance.objects.create(
            film=self.film,
            date_starts=datetime.date.today(),
            date_ends=datetime.date.today() + datetime.timedelta(days=30),
            time_starts=datetime.time(hour=23, minute=50),
            places_taken=0,
            hall=self.hall,
            is_active=True,
            description='Some text about why this seance is the best',
            ticket_price=100,
            admin=self.admin,
        )
        self.assertEqual(seance2.time_ends, datetime.time(1, 40))
