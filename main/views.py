
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Place, Hotel, Guide

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
        image = request.FILES.get('image')
        gallery_images = request.FILES.getlist('gallery')

        place = Place.objects.create(
            name=name,
            description=description,
            location=location,
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
    hotels = Hotel.objects.all()
    return render(request, 'main/hotels.html', {'hotels': hotels})



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
    return render(request, 'main/guides.html', {'guides': guides})
