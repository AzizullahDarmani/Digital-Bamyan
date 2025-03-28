
from django.shortcuts import render
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

def guides_list(request):
    guides = Guide.objects.all()
    return render(request, 'main/guides.html', {'guides': guides})
