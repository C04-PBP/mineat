from django import forms
from .models import Review
from django.utils.html import strip_tags

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tulis ulasan Anda...'}),
        }
