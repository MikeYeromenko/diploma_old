from django.urls import path


from seance.views import SeanceListView, RegisterUserView, UserLoginView, UserProfileView

app_name = 'seance'


urlpatterns = [
    path('accounts/profile/', UserProfileView.as_view(), name='profile'),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('', SeanceListView.as_view(), name='index'),

]
