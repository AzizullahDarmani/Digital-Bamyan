
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .models import Hotel, Room, HotelImage, HotelRating, FavoriteHotel
from django.forms import modelformset_factory

def is_superuser(user):
    return user.is_superuser

def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotel/hotel_list.html', {'hotels': hotels})

@login_required
@user_passes_test(is_superuser)
def add_hotel(request):
    RoomFormSet = modelformset_factory(Room, fields=('room_type', 'price'), extra=3)
    
    if request.method == 'POST':
        hotel = Hotel.objects.create(
            name=request.POST['name'],
            location=request.POST['location'],
            description=request.POST['description']
        )
        
        formset = RoomFormSet(request.POST)
        if formset.is_valid():
            rooms = formset.save(commit=False)
            for room in rooms:
                room.hotel = hotel
                room.save()
                
        for image in request.FILES.getlist('images'):
            HotelImage.objects.create(hotel=hotel, image=image)
            
        return redirect('hotel:hotel_list')
        
    formset = RoomFormSet(queryset=Room.objects.none())
    return render(request, 'hotel/add_hotel.html', {'formset': formset})

@login_required
def rate_hotel(request, hotel_id):
    if request.method == 'POST':
        hotel = get_object_or_404(Hotel, id=hotel_id)
        rating = int(request.POST.get('rating'))
        
        hotel_rating, created = HotelRating.objects.get_or_create(
            hotel=hotel,
            user=request.user,
            defaults={'rating': rating}
        )
        
        if not created:
            hotel_rating.rating = rating
            hotel_rating.save()
            
        hotel.update_rating(rating)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@login_required
def hotel_gallery(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    return render(request, 'hotel/hotel_gallery.html', {'hotel': hotel})

def toggle_favorite(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    favorite, created = FavoriteHotel.objects.get_or_create(
        hotel=hotel,
        user=request.user
    )
    
    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True
        
    return JsonResponse({'is_favorite': is_favorite})
