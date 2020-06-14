from django.views.generic import ListView, CreateView

from seance.models import Seance, AdvUser


class SeanceListView(ListView):
    model = Seance
    template_name = 'seance/index.html'


class RegisterUserView(CreateView):
    model = AdvUser

