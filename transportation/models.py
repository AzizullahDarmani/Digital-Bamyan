
from django.db import models
from django.core.validators import MinValueValidator

class Transportation(models.Model):
    VEHICLE_TYPES = (
        ('car', 'Car'),
        ('bus', 'Bus'),
        ('van', 'Van'),
        ('bike', 'Bike'),
    )

    name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='transportation/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.vehicle_type})"

class TransportationRental(models.Model):
    vehicle = models.ForeignKey(Transportation, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rental_date = models.DateField()
    return_date = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle.name} rented by {self.user.username}"
