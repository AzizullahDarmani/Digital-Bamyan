from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Place, Hotel, PlaceImage, FavoriteImage, PageVisit
from guides.models import Guide

def home(request):
    places = Place.objects.all()[:6]
    hotels = Hotel.objects.all()[:4]
    guides = Guide.objects.all()[:3]
    return render(request, 'main/home.html', {
        'places': places,
        'hotels': hotels,
        'guides': guides
    })

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator

def is_superuser(user):
    return user.is_superuser

def places_list(request):
    places = Place.objects.all().order_by('-created_at')
    paginator = Paginator(places, 12)
    page = request.GET.get('page')
    places = paginator.get_page(page)
    return render(request, 'main/places.html', {'places': places})

@user_passes_test(is_superuser)
def add_place(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        location = request.POST.get('location')
        location_url = request.POST.get('location_url')
        image = request.FILES.get('image')
        gallery_images = request.FILES.getlist('gallery')

        place = Place.objects.create(
            name=name,
            description=description,
            location=location,
            location_url=location_url,
            image=image
        )

        for img in gallery_images:
            place_image = PlaceImage.objects.create(image=img)
            place.gallery.add(place_image)

        return redirect('main:places')
    return render(request, 'main/add_place.html')

def place_detail(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    return render(request, 'main/place_detail.html', {'place': place})

@user_passes_test(is_superuser)
def edit_place(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    if request.method == 'POST':
        place.name = request.POST.get('name')
        place.description = request.POST.get('description')
        place.location = request.POST.get('location')
        place.location_url = request.POST.get('location_url')
        if 'image' in request.FILES:
            place.image = request.FILES['image']
        place.save()

        if 'gallery' in request.FILES:
            for img in request.FILES.getlist('gallery'):
                place_image = PlaceImage.objects.create(image=img)
                place.gallery.add(place_image)

        return redirect('main:places')
    return render(request, 'main/edit_place.html', {'place': place})

@user_passes_test(is_superuser)
def delete_place(request, place_id):
    if request.method == 'POST':
        place = get_object_or_404(Place, id=place_id)
        place.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def toggle_like(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    if request.user in place.likes.all():
        place.likes.remove(request.user)
        liked = False
    else:
        place.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'count': place.likes.count()})

@login_required
def toggle_favorite(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    if request.user in place.favorites.all():
        place.favorites.remove(request.user)
        favorited = False
    else:
        place.favorites.add(request.user)
        favorited = True
    return JsonResponse({'favorited': favorited})

def hotels_list(request):
    return redirect('/hotel/')



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:home')
    else:
        form = UserCreationForm()
    return render(request, 'main/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:home')
    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    return redirect('main:home')

def guides_list(request):
    guides = Guide.objects.all()
    return render(request, 'guides/guide_list.html', {'guides': guides})

@login_required
def place_gallery(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    return render(request, 'main/place_gallery.html', {'place': place})

@login_required
@user_passes_test(is_superuser)
def add_gallery_image(request, place_id):
    if request.method == 'POST':
        place = get_object_or_404(Place, id=place_id)
        images = request.FILES.getlist('images')
        for img in images:
            place_image = PlaceImage.objects.create(image=img)
            place.gallery.add(place_image)
        return redirect('main:place_gallery', place_id=place_id)
    return redirect('main:place_gallery', place_id=place_id)

@login_required
def toggle_favorite_image(request, image_id):
    image = get_object_or_404(PlaceImage, id=image_id)
    favorite, created = FavoriteImage.objects.get_or_create(
        user=request.user,
        image=image
    )
    if not created:
        favorite.delete()
    return JsonResponse({'favorited': created})

@login_required
def favorites(request):
    favorite_images = FavoriteImage.objects.filter(user=request.user).select_related('image')
    favorite_places = Place.objects.filter(favorites=request.user).prefetch_related('likes')
    return render(request, 'main/favorites.html', {
        'favorite_images': favorite_images,
        'favorite_places': favorite_places
    })

@login_required
@user_passes_test(is_superuser)
def delete_image(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(PlaceImage, id=image_id)
        image.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def about(request):
    return render(request, 'main/about.html')
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta
import json

@user_passes_test(is_superuser)
def analytics(request):
    # Get all users ordered by join date, excluding superusers
    users = User.objects.filter(is_superuser=False).order_by('-date_joined')
    
    # Get visits for the last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    visits = PageVisit.objects.filter(
        timestamp__gte=thirty_days_ago
    ).annotate(
        date=TruncDate('timestamp')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')
    
    # Prepare data for the chart
    dates = [visit['date'].strftime('%Y-%m-%d') for visit in visits]
    visit_counts = [visit['count'] for visit in visits]
    
    return render(request, 'main/analytics.html', {
        'users': users,
        'dates': json.dumps(dates),
        'visits': json.dumps(visit_counts)
    })

@user_passes_test(is_superuser)
def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        if not user.is_superuser:  # Prevent deleting superusers
            user.delete()
        return redirect('main:analytics')
    return redirect('main:analytics')
