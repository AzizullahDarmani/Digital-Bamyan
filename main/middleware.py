
from .models import PageVisit

class VisitTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Don't track static/media files and admin pages
        if not any(path in request.path for path in ['/static/', '/media/', '/admin/']):
            PageVisit.objects.create(
                path=request.path,
                user=request.user if request.user.is_authenticated else None,
                ip_address=request.META.get('REMOTE_ADDR')
            )
        
        return response
