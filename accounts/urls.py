from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetCompleteView #, PasswordChangeView
from .views import create_user, confirmation, logoff, get_profile,\
    edit_profile, ChangePasswordView, reset_password_confirm


app_name = 'accounts'
urlpatterns = [
    path('', create_user, name='accounts'),
    path('create/', create_user, name='create_user'),
    path('confirmation/<uidb64>/<token>/', confirmation, name='confirmation'),
    path('login/', LoginView.as_view(),
        {'template_name': 'accounts/login.html'}, name='login'),
    path('logout/', logoff, name='logout'),
    path('profile/', get_profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('reset_password/', PasswordResetView.as_view(
        success_url=reverse_lazy('accounts:password_reset_done'),
        template_name='reset_password.html',
        email_template_name='emails/reset_password_email.html',),
        name='reset_password'),
    path('password_reset_done/',PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'),
        name='password_reset_done'),
    path('reset_password_complete/',PasswordResetCompleteView.as_view(
        template_name='reset_password_complete.html'),
        name='reset_password_complete'
    ),
    path('reset/<uidb64>/<token>/',
         reset_password_confirm,
         name='password_reset_confirm'),
]
