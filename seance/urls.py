from django.urls import path


from seance.views import SeanceListView, RegisterUserView, UserLoginView, UserProfileView, UserLogoutView, BasketView

app_name = 'seance'

urlpatterns = [
    path('basket/', BasketView.as_view(), name='basket'),
    path('accounts/profile/', UserProfileView.as_view(), name='profile'),
    path('accounts/logout/', UserLogoutView.as_view(), name='logout'),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('', SeanceListView.as_view(), name='index'),

]
