
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('places/', views.places_list, name='places'),
    path('places/<int:place_id>/', views.place_detail, name='place_detail'),
    path('places/<int:place_id>/like/', views.toggle_like, name='toggle_like'),
    path('places/<int:place_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('hotels/', views.hotels_list, name='hotels'),
    path('guides/', views.guides_list, name='guides'),
]
