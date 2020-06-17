import datetime

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, TemplateView, FormView, DetailView, RedirectView

from seance.forms import RegistrationForm, OrderingForm
from seance.models import Seance, AdvUser, Hall


class SeanceListView(ListView):
    model = Seance
    template_name = 'seance/index.html'

    def get_queryset(self):
        query = Q(is_active=True)

        # if user wants to watch seances for tomorrow this key will be GET

        if self.request.GET.get('days', None):
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            query &= Q(date_starts__lte=tomorrow) & Q(date_ends__gte=tomorrow)
        else:
            query &= (Q(date_starts__lte=datetime.date.today()) & Q(date_ends__gte=datetime.date.today()) &
                      Q(time_starts__gt=timezone.now()))

        seances = Seance.objects.filter(query)

        # if user selected type of ordering
        ordering_param = self.request.GET.get('ordering', None)
        if ordering_param:
            seances = self.order_queryset(ordering_param, seances)
        return seances

    @staticmethod
    def order_queryset(ordering_param, seances):
        """
        orders seances queryset by users ordering
        """
        if ordering_param == 'cheap':
            return seances.order_by('ticket_price')
        elif ordering_param == 'expensive':
            return seances.order_by('-ticket_price')
        elif ordering_param == 'latest':
            return seances.order_by('-time_starts')
        elif ordering_param == 'closest':
            return seances.order_by('time_starts')

    def get_context_data(self, *args, **kwargs):
        """
        Adds OrderingForm to context
        :return: context
        """
        context = super().get_context_data(*args, **kwargs)

        # if there is a choice made by user, we render page with that choice
        ordering = self.request.GET.get('ordering', '')
        days = self.request.GET.get('days', '')
        ordering_form = OrderingForm(initial={'ordering': ordering, 'days': days})

        context['ordering_form'] = ordering_form
        return context


class SeanceDetailView(DetailView):
    model = Seance
    template_name = 'seance/seance_detail.html'


class RegisterUserView(CreateView):
    model = AdvUser
    form_class = RegistrationForm
    template_name = 'registration/register_user.html'
    success_url = reverse_lazy('seance:index')


class UserLoginView(LoginView):

    def form_valid(self, form):
        """
        Security check complete. Log the user in.
        Updates last_activity field
        """
        user = get_object_or_404(AdvUser, pk=form.get_user().pk)
        user.last_activity = timezone.now()
        user.save()
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class UserLogoutView(LogoutView):
    pass


class UserProfileView(TemplateView):
    template_name = 'seance/profile.html'


class BasketView(LoginRequiredMixin, TemplateView):
    template_name = 'seance/basket.html'


class BasketRedirectView(LoginRequiredMixin, RedirectView):
    pattern_name = 'seance:basket'
    
    def dispatch(self, request, *args, **kwargs):
        row = request.GET.get('row', None)
        seat = request.GET.get('seat', None)
        seance_pk = request.GET.get('seance', None)
        if row and seat and seance_pk:
            if not request.session.get('basket', None):
                request.session['basket'] = {}
            seance = get_object_or_404(Seance, pk=seance_pk)
            request.session['basket'][f'{timezone.now()}'] = {
                'row': row,
                'seat': seat,
                'seance_pk': seance_pk,
                'film': seance.film.title,
                'hall': seance.hall.name
            }
            request.session.modified = True
        # for bas in request.session["basket"]:
        #     print(f'!!!!!!!!{request.session["basket"][bas]}')
        return super(BasketRedirectView, self).dispatch(request, *args, **kwargs)


