
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Avg
from .models import Guide, GuideReview
from django.http import JsonResponse

def is_superuser(user):
    return user.is_superuser

def guide_list(request):
    guides = Guide.objects.all().order_by('-created_at')
    print(f"Found {guides.count()} guides")  # Debug print
    for guide in guides:
        print(f"Guide: {guide.full_name}, Photo: {guide.photo.url if guide.photo else 'No photo'}")
        try:
            avg_rating = guide.reviews.aggregate(Avg('rating'))['rating__avg']
            guide.avg_rating = avg_rating if avg_rating else 0
        except Exception as e:
            guide.avg_rating = 0
            print(f"Error calculating rating for guide {guide.full_name}: {str(e)}")
    return render(request, 'guides/guide_list.html', {'guides': guides})

@user_passes_test(is_superuser)
def add_guide(request):
    if request.method == 'POST':
        try:
            languages = request.POST.getlist('languages')
            if not languages:
                messages.error(request, 'Please select at least one language')
                return render(request, 'guides/add_guide.html', {'guide': Guide})
            
            guide = Guide.objects.create(
                full_name=request.POST['full_name'],
                photo=request.FILES.get('photo'),
                description=request.POST['description'],
                experience_years=int(request.POST['experience_years']),
                languages=languages,
                contact_number=request.POST['contact_number'],
                hourly_rate=float(request.POST['hourly_rate'])
            )
            messages.success(request, 'Guide added successfully!')
            return redirect('guides:guide_list')
        except Exception as e:
            messages.error(request, f'Error adding guide: {str(e)}')
            return render(request, 'guides/add_guide.html', {'guide': Guide})
    return render(request, 'guides/add_guide.html', {'guide': Guide})

@user_passes_test(is_superuser)
def delete_guide(request, guide_id):
    guide = get_object_or_404(Guide, id=guide_id)
    guide.delete()
    messages.success(request, 'Guide deleted successfully!')
    return redirect('guides:guide_list')

@user_passes_test(is_superuser)
def edit_guide(request, guide_id):
    guide = get_object_or_404(Guide, id=guide_id)
    if request.method == 'POST':
        try:
            languages = request.POST.getlist('languages')
            if not languages:
                messages.error(request, 'Please select at least one language')
                return render(request, 'guides/edit_guide.html', {'guide': guide})
            
            guide.full_name = request.POST['full_name']
            if 'photo' in request.FILES:
                guide.photo = request.FILES['photo']
            guide.description = request.POST['description']
            guide.experience_years = int(request.POST['experience_years'])
            guide.languages = languages
            guide.contact_number = request.POST['contact_number']
            guide.hourly_rate = float(request.POST['hourly_rate'])
            guide.save()
            
            messages.success(request, 'Guide updated successfully!')
            return redirect('guides:guide_list')
        except Exception as e:
            messages.error(request, f'Error updating guide: {str(e)}')
            return render(request, 'guides/edit_guide.html', {'guide': guide})
    return render(request, 'guides/edit_guide.html', {'guide': guide})

@login_required
def rate_guide(request, guide_id):
    guide = get_object_or_404(Guide, id=guide_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        review, created = GuideReview.objects.update_or_create(
            guide=guide,
            user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
