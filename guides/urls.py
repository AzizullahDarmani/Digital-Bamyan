
from django.urls import path
from . import views

app_name = 'guides'

urlpatterns = [
    path('', views.guide_list, name='guide_list'),
    path('<int:guide_id>/rate/', views.rate_guide, name='rate_guide'),
]
