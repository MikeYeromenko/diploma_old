from django.urls import path


from seance.views import SeanceListView, RegisterUserView, UserLoginView, UserProfileView, UserLogoutView, BasketView, \
    SeanceDetailView, BasketRedirectView

app_name = 'seance'

urlpatterns = [
    path('basket/redirect/', BasketRedirectView.as_view(), name='basket-redirect'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('accounts/profile/', UserProfileView.as_view(), name='profile'),
    path('accounts/logout/', UserLogoutView.as_view(), name='logout'),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('seance/<int:pk>/', SeanceDetailView.as_view(), name='seance_detail'),
    path('', SeanceListView.as_view(), name='index'),

]
