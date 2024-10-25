from django import forms
from fnb.models import Fnb
from ingredient.models import Ingredient

class FnbForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),  # Query all ingredients
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Fnb
        fields = ["name", "description", "price"]  # Include the ingredients field


    # def clean_mood(self):
    #     mood = self.cleaned_data["mood"]
    #     return strip_tags(mood)

    # def clean_feelings(self):
    #     feelings = self.cleaned_data["feelings"]
    #     return strip_tags(feelings)