
from django.urls import path
from . import views

app_name = 'hotels'

urlpatterns = [
    path('', views.hotels_list, name='hotels_list'),
    path('add/', views.add_hotel, name='add_hotel'),
    path('<int:hotel_id>/edit/', views.edit_hotel, name='edit_hotel'),
    path('<int:hotel_id>/delete/', views.delete_hotel, name='delete_hotel'),
]
