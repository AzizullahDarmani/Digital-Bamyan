
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Avg
from .models import Hotel, HotelReview, HotelBooking
from django.contrib import messages

def hotel_list(request):
    hotels = Hotel.objects.all().annotate(avg_rating=Avg('reviews__rating'))
    return render(request, 'hotel/hotel_list.html', {'hotels': hotels})

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
        rating = request.POST.get('rating')
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
            
        hotel.rating = hotel.reviews.aggregate(Avg('rating'))['rating__avg']
        hotel.save()
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def book_hotel(request, hotel_id):
    if request.method == 'POST':
        hotel = get_object_or_404(Hotel, id=hotel_id)
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        
        booking = HotelBooking.objects.create(
            hotel=hotel,
            user=request.user,
            check_in=check_in,
            check_out=check_out
        )
        
        messages.success(request, 'Hotel booked successfully!')
        return redirect('hotel:hotel_list')
    return JsonResponse({'success': False})
