from django import forms
from .models import Restaurant, Rating, Sale

class RestaurantCreationForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'website', 'latitude', 'longitude', 'restaurant_type', 'opened_at']
        widgets = {
            'opened_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'restaurant_type': forms.Select(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'name': 'Enter the name of the restaurant.',
            'website': 'Enter the website URL of the restaurant (optional).',
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }
        help_texts = {
            'score': 'Enter a rating score between 1 and 5.',
        }

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['income', 'date']
        widgets = {
            'income': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
        help_texts = {
            'income': 'Enter the sale amount.',
            'date': 'Enter the date and time of the sale.',
        }