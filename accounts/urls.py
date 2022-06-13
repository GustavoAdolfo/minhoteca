from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, \
    PasswordResetDoneView, \
    PasswordResetCompleteView, PasswordChangeView
from .views import create_user, confirmation, logoff


app_name = 'accounts'
urlpatterns = [
    path('', create_user, name='accounts'),
    path('create/', create_user, name='create_user'),
    path('confirmation/<uidb64>/<token>/', confirmation, name='confirmation'),
    path('login/', LoginView.as_view(),
        {'template_name': 'accounts/login.html'}, name='login'),
    path('password_reset/', PasswordResetView.as_view(
        success_url=reverse_lazy('accounts:password_reset_done'),
        template_name='accounts/password_reset.html'),
        name='password_reset'),
    path('logout/', logoff, name='logout'),
]
