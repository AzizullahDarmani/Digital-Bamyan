
from django.urls import path
from . import views

app_name = 'hotel'

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),
    path('add/', views.add_hotel, name='add_hotel'),
    path('<int:hotel_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('<int:hotel_id>/rate/', views.rate_hotel, name='rate_hotel'),
    path('<int:hotel_id>/book/', views.book_hotel, name='book_hotel'),
]
