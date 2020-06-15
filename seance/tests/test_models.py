import datetime
from django.contrib.auth import get_user_model
from django.db.models import ProtectedError
from django.test import TestCase
from django.utils import timezone

from seance.models import Film, Hall, Seance, AdvUser


class BaseInitial:
    def __init__(self):
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


class SeanceModelsTestCase(TestCase, BaseInitial):

    def setUp(self):
        BaseInitial.__init__(self)

    def test_film_model_basic(self):
        """
        Tests that Film object was created correctly
        """
        self.assertEqual(self.film.title, 'James Bond')
        self.assertEqual(self.film.starring, 'Daniel Craig and co')
        self.assertEqual(self.film.director, 'Director')
        self.assertEqual(self.film.description, 'some text....')
        self.assertEqual(self.film.duration, datetime.time(1, 40))
        self.assertEqual(self.film.admin.username, 'admin')
        self.assertTrue(self.film.is_active)

        # film was created no more then 2 minutes ago
        self.assertTrue(timezone.now() - datetime.timedelta(minutes=2) < self.film.created < timezone.now())

    def test_hall_model_basic(self):
        """
        Tests that Hall object was created correctly
        """
        self.assertEqual(self.hall.name, 'Yellow')
        self.assertEqual(self.hall.size, 50)
        self.assertEqual(self.hall.admin.username, 'admin')
        self.assertEqual(self.hall.description, 'Some text about why this hall is the best')
        self.assertTrue(self.hall.is_active)

        # hall was created no more then 2 minutes ago
        self.assertTrue(timezone.now() - datetime.timedelta(minutes=2) < self.hall.created < timezone.now())

    def test_seance_model_basic(self):
        """
        Tests that Seance object was created correctly
        """
        self.assertEqual(self.seance.film.title, 'James Bond')
        self.assertEqual(self.seance.date_starts, datetime.date.today())
        self.assertEqual(self.seance.date_ends, datetime.date.today() + datetime.timedelta(days=15))
        self.assertEqual(self.seance.time_starts, datetime.time(12))
        self.assertEqual(self.seance.ticket_price, 100)
        self.assertEqual(self.seance.time_ends, datetime.time(13, 50))
        self.assertEqual(self.seance.hall.name, 'Yellow')
        self.assertEqual(self.seance.places_taken, 0)
        self.assertEqual(self.seance.description, 'Some text about why this seance is the best')
        self.assertTrue(self.seance.is_active)
        self.assertEqual(self.seance.admin.username, 'admin')

        # seance was created no more then 2 minutes ago
        self.assertTrue(timezone.now() - datetime.timedelta(minutes=2) < self.seance.created < timezone.now())

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
        # create new seance object based on self.seance with new time_starts. time_ends will be
        # 24 hours and 50 minutes (+10min for advertisement). Here we check it will become 0 hour 50 minutes
        seance1 = Seance.objects.create(
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
        self.assertEqual(seance1.time_ends, datetime.time(0, 50))

        # create new seance object based on self.seance with new time_starts. time_ends will be
        # 24 hours and 100 minutes (+10min for advertisement). Here we check it will become 1 hour 40 minutes
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

        #   Test if in Yellow hall there are 3 seances
        self.assertEqual(Seance.objects.filter(hall=self.hall).count(), 3)

    def test_admin_created(self):
        """
        Test if user was created, with initial data
        """
        self.assertEqual(self.admin.username, 'admin')
        self.assertTrue(self.admin.is_superuser)
        self.assertTrue(self.admin.is_staff)
        #   Test user's type class has name AdvUser
        self.assertEqual(type(self.admin).__name__, 'AdvUser')

    def test_admin_cannot_be_deleted(self):
        """
        We can't delete admin. If we del, admin.is_active becomes False, but instance is left at database
        """
        admin2 = AdvUser.objects.create_superuser(username='admin2', email='admin2@some_site.com')
        admin2.set_password('password2')
        admin2.save()
        self.assertTrue(admin2.is_active)
        admin2.delete()
        self.assertFalse(admin2.is_active)
        self.assertTrue(admin2.was_deleted)
        self.assertTrue(AdvUser.objects.filter(username='admin2'))

    def test_user_created_and_deleted(self):
        """
        Test that user is created correctly
        """
        user = AdvUser.objects.create(
            username='user1',
            email='user1@somesite.com',
            first_name='Mike',
            last_name='Yeromenko',
            wallet=10000,
        )
        user.set_password('password2')
        user.save()
        self.assertEqual(user.username, 'user1')
        self.assertEqual(user.email, 'user1@somesite.com')
        self.assertEqual(user.first_name, 'Mike')
        self.assertEqual(user.last_name, 'Yeromenko')
        self.assertEqual(user.wallet, 10000.00)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

        # user was created no more then 2 minutes ago
        self.assertTrue(timezone.now() - datetime.timedelta(minutes=2) < user.date_joined < timezone.now())

        # user's last activity field was set by default
        self.assertTrue(timezone.now() - datetime.timedelta(minutes=1) < user.last_activity < timezone.now())

        # inbuilt methods give what we expect
        self.assertEqual(user.get_full_name(), 'Mike Yeromenko')
        self.assertEqual(user.get_short_name(), 'Mike')

        # after deletion of user it's not deleted, but just gets attribute is_active=False
        # and was_deleted=True
        user.delete()
        self.assertTrue(user.was_deleted)
        self.assertFalse(user.is_active)

    def test_instances_can_be_deleted(self):
        """
        Test if we can delete Seance, Hall, Film and AdvUser objects object
        """
        # We can't delete Film object, if there are seance references on it
        with self.assertRaises(ProtectedError):
            Film.objects.last().delete()

        # We can't delete Hall object, if there are seance references on it
        with self.assertRaises(ProtectedError):
            Hall.objects.last().delete()

        # delete seance object, but before watch it exists
        self.assertEqual(Seance.objects.all().count(), 1)
        Seance.objects.last().delete()
        self.assertEqual(Seance.objects.all().count(), 0)

        # after that Film and Hall objects can be deleted
        Film.objects.last().delete()
        Hall.objects.last().delete()

        self.assertEqual(Film.objects.all().count(), 0)
        self.assertEqual(Hall.objects.all().count(), 0)

