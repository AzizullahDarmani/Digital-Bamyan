
from django.db import models
from django.contrib.auth.models import User

class GuideReview(models.Model):
    guide = models.ForeignKey('main.Guide', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('guide', 'user')
