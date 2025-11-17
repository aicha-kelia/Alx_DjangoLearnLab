from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:book_id>/', views.view_book, name='view_book'),
    path('book/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('books/', views.book_list, name='book_list'),
]
