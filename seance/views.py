from django.views.generic import ListView


class SeanceListView(ListView):
    template_name = 'seance/index.html'
