
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Transportation, TransportationRental, TransportationImage
from django.contrib import messages
from datetime import datetime

def is_superuser(user):
    return user.is_superuser

def transportation_list(request):
    vehicles = Transportation.objects.filter(available=True)
    return render(request, 'transportation/transportation_list.html', {'vehicles': vehicles})

@user_passes_test(is_superuser)
def add_transportation(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        vehicle_type = request.POST.get('vehicle_type')
        capacity = request.POST.get('capacity')
        price_per_day = request.POST.get('price_per_day')
        description = request.POST.get('description')
        images = request.FILES.getlist('images')
        
        vehicle = Transportation.objects.create(
            name=name,
            vehicle_type=vehicle_type,
            capacity=capacity,
            price_per_day=price_per_day,
            description=description,
            image=images[0] if images else None
        )

        # Create TransportationImage objects for additional images
        for image in images[1:]:
            TransportationImage.objects.create(
                vehicle=vehicle,
                image=image
            )
        messages.success(request, 'Vehicle added successfully!')
        return redirect('transportation:transportation_list')
        
    return render(request, 'transportation/add_transportation.html')

@login_required
def rent_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Transportation, id=vehicle_id)
    if request.method == 'POST':
        rental_date = request.POST.get('rental_date')
        return_date = request.POST.get('return_date')
        days = (datetime.strptime(return_date, '%Y-%m-%d') - datetime.strptime(rental_date, '%Y-%m-%d')).days
        total_cost = vehicle.price_per_day * days

        TransportationRental.objects.create(
            vehicle=vehicle,
            user=request.user,
            rental_date=rental_date,
            return_date=return_date,
            total_cost=total_cost
        )
        vehicle.available = False
        vehicle.save()
        messages.success(request, 'Vehicle rented successfully!')
        return redirect('transportation:my_rentals')
    return render(request, 'transportation/rent_vehicle.html', {'vehicle': vehicle})

@login_required
def my_rentals(request):
    if request.user.is_superuser:
        rentals = TransportationRental.objects.all().order_by('-created_at')
    else:
        rentals = TransportationRental.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'transportation/my_rentals.html', {'rentals': rentals})

@user_passes_test(is_superuser)
def edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Transportation, id=vehicle_id)
    if request.method == 'POST':
        vehicle.name = request.POST.get('name')
        vehicle.vehicle_type = request.POST.get('vehicle_type')
        vehicle.capacity = request.POST.get('capacity')
        vehicle.price_per_day = request.POST.get('price_per_day')
        vehicle.description = request.POST.get('description')
        if 'image' in request.FILES:
            vehicle.image = request.FILES['image']
        vehicle.save()
        messages.success(request, 'Vehicle updated successfully!')
        return redirect('transportation:transportation_list')
    return render(request, 'transportation/edit_vehicle.html', {'vehicle': vehicle})

@user_passes_test(is_superuser)
def delete_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Transportation, id=vehicle_id)
    vehicle.delete()
    messages.success(request, 'Vehicle deleted successfully!')
    return redirect('transportation:transportation_list')
