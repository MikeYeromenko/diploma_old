from django.urls import path


from seance.views import SeanceListView, RegisterUserView, UserLoginView, UserProfileView, UserLogoutView


app_name = 'seance'

urlpatterns = [
    path('accounts/profile/', UserProfileView.as_view(), name='profile'),
    path('accounts/logout/', UserLogoutView.as_view(), name='logout'),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('<str:ordering>/', SeanceListView.as_view(), name='index_with_ordering'),
    path('', SeanceListView.as_view(), name='index'),

]
