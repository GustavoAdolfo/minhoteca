from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.index, name='books'),
    path('search/', views.search_books, name='search'),
    path('book/<int:pk>/', views.book, name='book'),
    path('author/<int:pk>/', views.author, name='author')
]
