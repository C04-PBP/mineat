from django import forms
from .models import Restaurant, Location, Fnb

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'image', 'address', 'location', 'fnb']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # For location, show the name instead of object representation
        self.fields['location'].queryset = Location.objects.all()
        self.fields['location'].label_from_instance = lambda obj: obj.name

        # For fnb, show the names instead of object representation
        self.fields['fnb'].required = False
        self.fields['fnb'].widget = forms.CheckboxSelectMultiple()
        self.fields['fnb'].queryset = Fnb.objects.all()
        self.fields['fnb'].label_from_instance = lambda obj: obj.name