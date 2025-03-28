
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('places/', views.places_list, name='places'),
    path('hotels/', views.hotels_list, name='hotels'),
    path('guides/', views.guides_list, name='guides'),
]
