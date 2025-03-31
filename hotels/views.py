from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Hotel

def is_superuser(user):
    return user.is_superuser

def hotels_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotels/hotels.html', {'hotels': hotels})

@user_passes_test(is_superuser)
def add_hotel(request):
    if request.method == 'POST':
        hotel = Hotel.objects.create(
            name=request.POST['name'],
            description=request.POST['description'],
            city=request.POST['city'],
            address=request.POST['address'],
            price_per_night=request.POST['price_per_night'],
            star_rating=request.POST['star_rating'],
            phone=request.POST['phone'],
            email=request.POST['email'],
            website=request.POST.get('website', ''),
            main_image=request.FILES['main_image']
        )
        return redirect('hotels:hotels_list')
    return render(request, 'hotels/add_hotel.html')

@user_passes_test(is_superuser)
def edit_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    if request.method == 'POST':
        hotel.name = request.POST['name']
        hotel.description = request.POST['description']
        hotel.city = request.POST['city']
        hotel.address = request.POST['address']
        hotel.price_per_night = request.POST['price_per_night']
        hotel.star_rating = request.POST['star_rating']
        hotel.phone = request.POST['phone']
        hotel.email = request.POST['email']
        hotel.website = request.POST.get('website', '')
        if 'main_image' in request.FILES:
            hotel.main_image = request.FILES['main_image']
        hotel.save()
        return redirect('hotels:hotels_list')
    return render(request, 'hotels/edit_hotel.html', {'hotel': hotel})

@user_passes_test(is_superuser)
def delete_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    if request.method == 'POST':
        hotel.delete()
        return redirect('hotels:hotels_list')
    return render(request, 'hotels/delete_hotel.html', {'hotel': hotel})
