from django.urls import path


from seance.views import SeanceListView


app_name = 'seance'


urlpatterns = [
    path('', SeanceListView.as_view(), name='index'),

]
