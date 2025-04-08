
from django import forms
from .models import Hotel, Room, HotelImage, HotelReview, HotelBooking

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'description', 'location_url']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['type', 'price']

RoomFormSet = forms.inlineformset_factory(
    Hotel, Room, form=RoomForm,
    extra=3, can_delete=True
)

class HotelImageForm(forms.ModelForm):
    class Meta:
        model = HotelImage
        fields = ['image']

HotelImageFormSet = forms.inlineformset_factory(
    Hotel, HotelImage, form=HotelImageForm,
    extra=3, can_delete=True
)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = HotelReview
        fields = ['rating', 'comment']

class BookingForm(forms.ModelForm):
    class Meta:
        model = HotelBooking
        fields = ['room', 'check_in', 'check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }
