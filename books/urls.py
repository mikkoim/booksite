from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('set_user', views.set_user, name='set_user'),
    path('books/', views.ListBooksView.as_view(), name='books-all')
]