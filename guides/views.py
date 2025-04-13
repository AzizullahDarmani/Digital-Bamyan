
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Avg
from .models import Guide, GuideReview
from django.http import JsonResponse

def is_superuser(user):
    return user.is_superuser

def guide_list(request):
    guides = Guide.objects.all().annotate(avg_rating=Avg('reviews__rating'))
    return render(request, 'guides/guide_list.html', {'guides': guides})

@user_passes_test(is_superuser)
def add_guide(request):
    if request.method == 'POST':
        try:
            languages = request.POST.getlist('languages')
            if not languages:
                messages.error(request, 'Please select at least one language')
                return render(request, 'guides/add_guide.html')
            
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
            return render(request, 'guides/add_guide.html')
    return render(request, 'guides/add_guide.html')

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
