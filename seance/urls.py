from django.urls import path


from seance.views import SeanceListView, RegisterUserView

app_name = 'seance'


urlpatterns = [
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('', SeanceListView.as_view(), name='index'),

]
