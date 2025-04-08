
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.db.models import Avg
from django.contrib import messages
from .models import Hotel, HotelReview, HotelBooking, HotelImage, Room
from .forms import HotelForm, HotelImageFormSet, RoomFormSet

def is_superuser(user):
    return user.is_superuser

def hotel_list(request):
    hotels = Hotel.objects.all().annotate(avg_rating=Avg('reviews__rating'))
    return render(request, 'hotel/hotel_list.html', {'hotels': hotels})

@user_passes_test(is_superuser)
def add_hotel(request):
    if request.method == 'POST':
        hotel_form = HotelForm(request.POST)
        image_formset = HotelImageFormSet(request.POST, request.FILES, queryset=HotelImage.objects.none())
        room_formset = RoomFormSet(request.POST, queryset=Room.objects.none())
        
        if hotel_form.is_valid() and image_formset.is_valid() and room_formset.is_valid():
            hotel = hotel_form.save()
            
            for image_form in image_formset:
                if image_form.cleaned_data.get('image'):
                    image = image_form.save(commit=False)
                    image.hotel = hotel
                    image.save()
            
            for room_form in room_formset:
                if room_form.cleaned_data.get('type'):
                    room = room_form.save(commit=False)
                    room.hotel = hotel
                    room.save()
            
            messages.success(request, 'Hotel added successfully!')
            return redirect('hotel:hotel_list')
    else:
        hotel_form = HotelForm()
        image_formset = HotelImageFormSet(queryset=HotelImage.objects.none())
        room_formset = RoomFormSet(queryset=Room.objects.none())
    
    return render(request, 'hotel/add_hotel.html', {
        'hotel_form': hotel_form,
        'image_formset': image_formset,
        'room_formset': room_formset
    })

def hotel_gallery(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    return render(request, 'hotel/hotel_gallery.html', {'hotel': hotel})

@login_required
def toggle_favorite(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    if request.user in hotel.favorites.all():
        hotel.favorites.remove(request.user)
        is_favorite = False
    else:
        hotel.favorites.add(request.user)
        is_favorite = True
    return JsonResponse({'is_favorite': is_favorite})

@login_required
def rate_hotel(request, hotel_id):
    if request.method == 'POST':
        hotel = get_object_or_404(Hotel, id=hotel_id)
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')
        
        review, created = HotelReview.objects.get_or_create(
            hotel=hotel,
            user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        
        if not created:
            review.rating = rating
            review.comment = comment
            review.save()
        
        hotel.rating = hotel.reviews.aggregate(Avg('rating'))['rating__avg'] or 0.0
        hotel.save()
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def book_hotel(request, hotel_id):
    if request.method == 'POST':
        hotel = get_object_or_404(Hotel, id=hotel_id)
        room_type = request.POST.get('room_type')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        
        HotelBooking.objects.create(
            hotel=hotel,
            user=request.user,
            check_in=check_in,
            check_out=check_out,
            room_type=room_type
        )
        
        return JsonResponse({'success': True})
    return render(request, 'hotel/book_hotel.html', {'hotel': get_object_or_404(Hotel, id=hotel_id)})
