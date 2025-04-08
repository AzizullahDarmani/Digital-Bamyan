
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price_range = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    amenities = models.TextField()
    image = models.ImageField(upload_to='hotels/')
    favorites = models.ManyToManyField(User, related_name='favorite_hotels', blank=True)
    rating = models.FloatField(default=0.0)
    
    def __str__(self):
        return self.name

class HotelReview(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('hotel', 'user')

class HotelBooking(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
