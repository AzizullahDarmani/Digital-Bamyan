
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .models import Hotel, Room, HotelImage, HotelRating, FavoriteHotel

def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotel/hotel_list.html', {'hotels': hotels})

@login_required
def hotel_gallery(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    return render(request, 'hotel/hotel_gallery.html', {'hotel': hotel})

@login_required
def toggle_favorite(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    favorite, created = FavoriteHotel.objects.get_or_create(
        user=request.user,
        hotel=hotel
    )
    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True
    return JsonResponse({'status': 'success', 'favorited': is_favorite})

@login_required
def rate_hotel(request, hotel_id):
    if request.method == 'POST':
        hotel = get_object_or_404(Hotel, id=hotel_id)
        rating = request.POST.get('rating')
        review = request.POST.get('review', '')
        
        hotel_rating, created = HotelRating.objects.get_or_create(
            user=request.user,
            hotel=hotel,
            defaults={'rating': rating, 'review': review}
        )
        
        if not created:
            hotel_rating.rating = rating
            hotel_rating.review = review
            hotel_rating.save()
        
        # Update hotel's average rating
        avg_rating = HotelRating.objects.filter(hotel=hotel).aggregate(models.Avg('rating'))['rating__avg']
        hotel.rating = avg_rating or 0
        hotel.save()
        
        return JsonResponse({'status': 'success', 'rating': avg_rating})
    return JsonResponse({'status': 'error'}, status=400)
