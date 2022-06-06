from django.urls import path
from .views import create_user, confirmation


app_name = 'accounts'
urlpatterns = [
    path('', create_user, name='accounts'),
    path('create/', create_user, name='create_user'),
    path('confirmation/', confirmation, name='confirmation'),
]
