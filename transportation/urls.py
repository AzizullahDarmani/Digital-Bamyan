
from django.urls import path
from . import views

app_name = 'transportation'

urlpatterns = [
    path('', views.transportation_list, name='transportation_list'),
    path('add/', views.add_transportation, name='add_transportation'),
    path('rent/<int:vehicle_id>/', views.rent_vehicle, name='rent_vehicle'),
    path('my-rentals/', views.my_rentals, name='my_rentals'),
    path('edit/<int:vehicle_id>/', views.edit_vehicle, name='edit_vehicle'),
    path('delete/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),
]
