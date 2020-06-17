import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class AdvUser(AbstractUser):
    email = models.EmailField(verbose_name=_('email address'), blank=True, null=True)
    wallet = models.FloatField(blank=True, null=True, verbose_name=_('wallet'))
    was_deleted = models.BooleanField(default=False, verbose_name=_('was deleted?'))
    last_activity = models.DateTimeField(auto_now_add=True, blank=True, null=True,
                                         verbose_name=_('user\'s last activity was: '))

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.was_deleted = True
        self.save()


class Film(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('title'))
    starring = models.CharField(max_length=200, verbose_name=_('starring'))
    director = models.CharField(max_length=100, verbose_name=_('director'))
    duration = models.TimeField(verbose_name=_('duration'))
    description = models.TextField(verbose_name=_('description'))
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('instance created at'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('instance updated at'))
    admin = models.ForeignKey(AdvUser, on_delete=models.PROTECT, verbose_name=_('instance created by'))
    is_active = models.BooleanField(default=True, verbose_name=_('in run?'))

    def __str__(self):
        return self.title


class Hall(models.Model):
    name = models.CharField(max_length=20, verbose_name=_('name'))
    seats = models.PositiveSmallIntegerField(default=0, verbose_name=_('how many seats?'))
    rows = models.PositiveSmallIntegerField(default=0, verbose_name=_('how many seats?'))
    description = models.TextField(verbose_name=_('description'))
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('instance created at'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('instance updated at'))
    admin = models.ForeignKey(AdvUser, on_delete=models.PROTECT, verbose_name=_('instance created by'),
                              related_name='halls')
    is_active = models.BooleanField(default=True, verbose_name=_('in run?'))

    def __str__(self):
        return self.name

    @property
    def get_size(self):
        return self.rows * self.seats


class Seance(models.Model):
    film = models.ForeignKey(Film, on_delete=models.PROTECT, related_name='seances', verbose_name=_('films'))
    date_starts = models.DateField(verbose_name=_('starts'))
    date_ends = models.DateField(null=True, blank=True, verbose_name=_('ends'))
    time_starts = models.TimeField(verbose_name=_('starts at: '))
    time_ends = models.TimeField(null=True, blank=True, verbose_name=_('ends at: '))
    places_taken = models.PositiveIntegerField(default=0, verbose_name=_('places taken'))
    hall = models.ForeignKey(Hall, on_delete=models.PROTECT, related_name='seances', verbose_name=_('hall'))
    description = models.TextField(verbose_name=_('description'))
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('instance created at'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('instance updated at'))
    admin = models.ForeignKey(AdvUser, on_delete=models.PROTECT, verbose_name=_('instance created by'))
    is_active = models.BooleanField(default=True, verbose_name=_('in run?'))
    ticket_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('ticket costs:'))

    def save(self, *args, **kwargs):
        """
        Adds date_ends and time_ends if they weren't added by admin
        """
        if not self.id:
            if not self.date_ends:
                # if admin didn't set the date_ends of seance, by default it is set to +15 days to
                # date_start of seance
                self.date_ends = self.get_date_ends()

            if not self.time_ends:
                self.time_ends = self.get_time_ends()

        super().save(*args, **kwargs)

    def get_date_ends(self):
        """
        Counts the date of seance ending, adding 15 days to its start
        :return: date_ends of seance
        """
        return self.date_starts + datetime.timedelta(days=15)

    def get_time_ends(self):
        """
        Sets time_ends field of seance, if it was noy set by admin, adding to time_starts the film's
        duration and 10 minutes for advertisements.
        Code here is used for us to get a readable time value, for example if time_starts is 23 hours,
        and film.duration is 2 hours, we'll set time_ends at 1 hour 10 minutes, but not at 25 hours 10 minutes
        """
        minutes = self.time_starts.minute + self.film.duration.minute + 10

        # if value of minutes is more then 60, add integer part of it to hours
        hours = (self.time_starts.hour + self.film.duration.hour + minutes // 60) % 24

        # fractional part will be less then 60, so we leave it as minutes value
        minutes %= 60
        time_ends = datetime.time(hour=hours, minute=minutes)
        return time_ends

    def __str__(self):
        return f'Seance with {self.film.title}'

    @staticmethod
    def validate_seances_intersect(hall_id, date_starts, time_starts, date_ends, time_ends):
        """
        Validates, that given seance doesn't intersect with others in time
        :returns True if our seance intersects with another, False if not
        """
        seances = Seance.objects.filter(Q(hall_id=hall_id) & Q(date_starts__lte=date_ends) &
                                        Q(date_ends__gte=date_starts) & Q(time_starts__lt=time_ends) &
                                        Q(time_ends__gt=time_starts))
        return bool(seances)

    class Meta:
        ordering = ('time_starts', )
        verbose_name = _('seance')
        verbose_name_plural = _('seances')

    def seat_free(self, row, seat):
        pass


class Purchase(models.Model):
    user = models.ForeignKey(AdvUser, on_delete=models.PROTECT, related_name='purchases', verbose_name=_('user'))
    total_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('payed:'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('instance created at'))
    was_returned = models.BooleanField(default=False, verbose_name=_('was returned?'))
    returned_at = models.DateTimeField(blank=True, null=True, verbose_name=_('returned at'))

    def __str__(self):
        return f'{self.user.username} at {self.created_at}'


class Ticket(models.Model):
    seance = models.ForeignKey(Seance, on_delete=models.PROTECT, related_name='tickets', verbose_name=_('ticket'))
    purchase = models.ForeignKey(Purchase, on_delete=models.PROTECT, related_name='tickets', verbose_name=_('purchase'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('instance created at'))
    seat_number = models.PositiveSmallIntegerField(default=0, blank=True, null=True, verbose_name=_('seat number'))
    row_number = models.PositiveSmallIntegerField(default=0, blank=True, null=True, verbose_name=_('row number'))

    def __str__(self):
        return self.seance.__str__()
