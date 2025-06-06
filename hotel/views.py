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
        hotel_form = HotelForm(request.POST)
        room_formset = RoomFormSet(request.POST, prefix='rooms')
        image_formset = HotelImageFormSet(request.POST, request.FILES, prefix='images')

        if hotel_form.is_valid() and room_formset.is_valid() and image_formset.is_valid():
            hotel = hotel_form.save()
            room_formset.instance = hotel
            room_formset.save()
            image_formset.instance = hotel
            image_formset.save()
            messages.success(request, 'Hotel added successfully!')
            return redirect('hotel:hotel_list')
    else:
        hotel_form = HotelForm()
        room_formset = RoomFormSet(prefix='rooms')
        image_formset = HotelImageFormSet(prefix='images')

    return render(request, 'hotel/add_hotel.html', {
        'hotel_form': hotel_form,
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

@login_required
def my_bookings(request):
    if request.user.is_superuser:
        bookings = HotelBooking.objects.all().order_by('-created_at')
    else:
        bookings = HotelBooking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'hotel/my_bookings.html', {'bookings': bookings})

@user_passes_test(is_superuser)
def delete_booking(request, booking_id):
    booking = get_object_or_404(HotelBooking, id=booking_id)
    booking.delete()
    messages.success(request, 'Booking deleted successfully!')
    return redirect('hotel:my_bookings')



@user_passes_test(is_superuser)
def delete_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    hotel.delete()
    messages.success(request, 'Hotel deleted successfully!')
    return redirect('hotel:hotel_list')

def hotel_gallery(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    return render(request, 'hotel/hotel_gallery.html', {'hotel': hotel})
