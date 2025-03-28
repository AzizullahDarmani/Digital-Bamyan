
from django.db import models
from django.contrib.auth.models import User

class Place(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='places/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

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
