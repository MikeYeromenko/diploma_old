from django.views.generic import ListView, CreateView

from seance.forms import RegistrationForm
from seance.models import Seance, AdvUser


class SeanceListView(ListView):
    model = Seance
    template_name = 'seance/index.html'


class RegisterUserView(CreateView):
    model = AdvUser
    form_class = RegistrationForm
    template_name = 'seance/register_user.html'

