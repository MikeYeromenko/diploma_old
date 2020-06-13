from django.views.generic import ListView

from seance.models import Seance


class SeanceListView(ListView):
    model = Seance
    template_name = 'seance/index.html'

