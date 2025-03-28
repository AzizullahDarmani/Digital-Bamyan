
from django.db import models
from django.contrib.auth.models import User

class Place(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    location_url = models.URLField(max_length=500, blank=True, help_text="URL to location on map")
    image = models.ImageField(upload_to='places/', verbose_name='Main Image')
    gallery = models.ManyToManyField('PlaceImage', blank=True)
    rating = models.FloatField(default=0.0)
    likes = models.ManyToManyField('auth.User', related_name='liked_places', blank=True)
    favorites = models.ManyToManyField('auth.User', related_name='favorite_places', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class PlaceImage(models.Model):
    image = models.ImageField(upload_to='places/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"Image for {self.place_set.first()}"

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price_range = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    amenities = models.TextField()
    image = models.ImageField(upload_to='hotels/')
    
    def __str__(self):
        return self.name

class Guide(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    bio = models.TextField()
    photo = models.ImageField(upload_to='guides/')
    rating = models.FloatField(default=0.0)
    
    def __str__(self):
        return self.user.get_full_name()
