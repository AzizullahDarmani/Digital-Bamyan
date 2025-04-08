
from django import forms
from .models import Hotel, Room, HotelImage

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'description', 'location_url', 'amenities']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['type', 'price']

class HotelImageForm(forms.ModelForm):
    class Meta:
        model = HotelImage
        fields = ['image']
HotelImageFormSet = forms.modelformset_factory(HotelImage, form=HotelImageForm, extra=3)
RoomFormSet = forms.modelformset_factory(Room, form=RoomForm, extra=3)
