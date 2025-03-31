
from django.contrib import admin
from .models import Hotel, HotelImage, Room, Amenity, Review, Booking

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'star_rating', 'price_per_night')
    search_fields = ('name', 'description', 'city')
    list_filter = ('star_rating', 'city')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'room_type', 'price', 'available')
    list_filter = ('room_type', 'available', 'hotel')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'user', 'rating', 'created_at', 'is_approved')
    list_filter = ('rating', 'is_approved', 'created_at')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = "Approve selected reviews"

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'user', 'check_in', 'check_out', 'status')
    list_filter = ('status', 'check_in', 'check_out')

admin.site.register(HotelImage)
admin.site.register(Amenity)
