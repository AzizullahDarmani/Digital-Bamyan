
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Transportation
from django.contrib import messages

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
        image = request.FILES.get('image')
        
        Transportation.objects.create(
            name=name,
            vehicle_type=vehicle_type,
            capacity=capacity,
            price_per_day=price_per_day,
            description=description,
            image=image
        )
        messages.success(request, 'Vehicle added successfully!')
        return redirect('transportation:transportation_list')
        
    return render(request, 'transportation/add_transportation.html')
