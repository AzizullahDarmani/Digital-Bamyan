
from django.urls import path
from . import views

app_name = 'transportation'

urlpatterns = [
    path('', views.transportation_list, name='transportation_list'),
    path('add/', views.add_transportation, name='add_transportation'),
]
