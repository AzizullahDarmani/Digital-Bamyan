
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from main.models import Guide
from .models import GuideReview
from django.http import JsonResponse
from django.db.models import Avg

def guide_list(request):
    guides = Guide.objects.all().annotate(avg_rating=Avg('reviews__rating'))
    return render(request, 'guides/guide_list.html', {'guides': guides})

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
        
        # Update guide rating
        avg_rating = guide.reviews.aggregate(Avg('rating'))['rating__avg']
        guide.rating = avg_rating or 0
        guide.save()
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
