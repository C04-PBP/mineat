from django.forms import ModelForm
from fnb.models import Fnb
from django.utils.html import strip_tags

class FnbForm(ModelForm):
    class Meta:
        model = Fnb
        fields = ["name", "description", "price"]

    # def clean_mood(self):
    #     mood = self.cleaned_data["mood"]
    #     return strip_tags(mood)

    # def clean_feelings(self):
    #     feelings = self.cleaned_data["feelings"]
    #     return strip_tags(feelings)