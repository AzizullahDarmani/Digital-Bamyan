
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Guide(models.Model):
    LANGUAGE_CHOICES = [
        ('EN', 'English'),
        ('FA', 'Farsi'),
        ('PS', 'Pashto'),
        ('AR', 'Arabic'),
        ('UR', 'Urdu'),
    ]
    
    full_name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='guides/', null=True, blank=True)
    description = models.TextField()
    experience_years = models.PositiveIntegerField()
    languages = models.JSONField(default=list)  # Store multiple languages as a list
    contact_number = models.CharField(max_length=20)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.full_name

class GuideReview(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('guide', 'user')
