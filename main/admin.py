
from django.contrib import admin
from .models import Place, Hotel, Guide, PlaceImage

class PlaceImageInline(admin.TabularInline):
    model = Place.gallery.through
    extra = 1

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating', 'created_at')
    search_fields = ('name', 'description', 'location')
    inlines = [PlaceImageInline]
    exclude = ('gallery',)

admin.site.register(PlaceImage)
admin.site.register(Hotel)
admin.site.register(Guide)
admin.site.register(FavoriteImage)
