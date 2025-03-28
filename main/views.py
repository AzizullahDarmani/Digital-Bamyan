
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

def places_list(request):
    places = Place.objects.all()
    return render(request, 'main/places.html', {'places': places})

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
    return render(request, 'main/signup.html')

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
