import datetime

from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, TemplateView, FormView

from seance.forms import RegistrationForm, FilterForm
from seance.models import Seance, AdvUser


class SeanceListView(ListView):
    model = Seance
    template_name = 'seance/index.html'

    def get_queryset(self):
        return Seance.objects.filter(Q(is_active=True) &
                                     Q(date_starts__lte=datetime.date.today()) &
                                     Q(date_ends__gte=datetime.date.today()) &
                                     Q(time_starts__gt=timezone.now()))

    def get_context_data(self, *args, **kwargs):
        """
        Adds FilterForm to context
        :return: context
        """
        context = super().get_context_data(*args, **kwargs)
        form = FilterForm()
        context['filter_form'] = form
        return context


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
