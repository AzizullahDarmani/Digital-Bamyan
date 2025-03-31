
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('places/', views.places_list, name='places'),
    path('places/add/', views.add_place, name='add_place'),
    path('places/<int:place_id>/', views.place_detail, name='place_detail'),
    path('places/<int:place_id>/edit/', views.edit_place, name='edit_place'),
    path('places/<int:place_id>/delete/', views.delete_place, name='delete_place'),
    path('places/<int:place_id>/like/', views.toggle_like, name='toggle_like'),
    path('places/<int:place_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('hotels/', views.hotels_list, name='hotels'),
    path('guides/', views.guides_list, name='guides'),
    path('places/<int:place_id>/gallery/', views.place_gallery, name='place_gallery'),
    path('places/<int:place_id>/gallery/add/', views.add_gallery_image, name='add_gallery_image'),
    path('images/<int:image_id>/favorite/', views.toggle_favorite_image, name='toggle_favorite_image'),
    path('places/gallery/images/<int:image_id>/delete/', views.delete_image, name='delete_image'),
    path('favorites/', views.favorites, name='favorites'),
]
