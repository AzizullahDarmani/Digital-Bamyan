from django.contrib import admin
from .models import Transportation, TransportationRental, TransportationImage

class TransportationImageInline(admin.TabularInline):
    model = TransportationImage
    extra = 3

class TransportationAdmin(admin.ModelAdmin):
    inlines = [TransportationImageInline]

admin.site.register(Transportation, TransportationAdmin)
admin.site.register(TransportationRental)