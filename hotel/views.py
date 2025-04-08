from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.db.models import Avg
from django.contrib import messages
from .models import Hotel, HotelReview, HotelBooking, Room
from .forms import HotelForm, RoomFormSet, HotelImageFormSet, ReviewForm, BookingForm

def is_superuser(user):
    return user.is_superuser

def hotel_list(request):
    hotels = Hotel.objects.all().annotate(avg_rating=Avg('reviews__rating'))
    return render(request, 'hotel/hotel_list.html', {'hotels': hotels})

@user_passes_test(is_superuser)
def add_hotel(request):
    if request.method == 'POST':
        form = HotelForm(request.POST)
        room_formset = RoomFormSet(request.POST, prefix='rooms')
        image_formset = HotelImageFormSet(request.POST, request.FILES, prefix='images')

        if form.is_valid() and room_formset.is_valid() and image_formset.is_valid():
            hotel = form.save()
            room_formset.instance = hotel
            room_formset.save()
            image_formset.instance = hotel
            image_formset.save()
            messages.success(request, 'Hotel added successfully!')
            return redirect('hotel:hotel_list')
    else:
        form = HotelForm()
        room_formset = RoomFormSet(prefix='rooms')
        image_formset = HotelImageFormSet(prefix='images')

    return render(request, 'hotel/add_hotel.html', {
        'form': form,
        'room_formset': room_formset,
        'image_formset': image_formset
    })

@login_required
def toggle_favorite(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    if hotel.favorites.filter(id=request.user.id).exists():
        hotel.favorites.remove(request.user)
        is_favorite = False
    else:
        hotel.favorites.add(request.user)
        is_favorite = True
    return JsonResponse({'is_favorite': is_favorite})

@login_required
def rate_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.hotel = hotel
            review.user = request.user
            review.save()

            # Update hotel rating
            avg_rating = hotel.reviews.aggregate(Avg('rating'))['rating__avg']
            hotel.rating = avg_rating
            hotel.save()

            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def book_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        form.fields['room'].queryset = hotel.rooms.all()

        if form.is_valid():
            booking = form.save(commit=False)
            booking.hotel = hotel
            booking.user = request.user
            booking.save()
            messages.success(request, 'Booking confirmed successfully!')
            return redirect('hotel:hotel_list')

    else:
        form = BookingForm()
        form.fields['room'].queryset = hotel.rooms.all()

    return render(request, 'hotel/book_hotel.html', {
        'form': form,
        'hotel': hotel
    })



def hotel_gallery(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    return render(request, 'hotel/hotel_gallery.html', {'hotel': hotel})
