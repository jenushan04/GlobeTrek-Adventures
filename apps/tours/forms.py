"""Forms for the tours app — staff CRUD + customer reviews."""
from django import forms
from .models import TourPackage, Destination, Review


class TourPackageForm(forms.ModelForm):
    """Staff form for creating/editing tour packages."""

    class Meta:
        model = TourPackage
        fields = [
            'title', 'destination', 'category', 'description',
            'duration_days', 'price', 'max_travellers',
            'includes', 'excludes', 'image', 'rating',
            'available_from', 'available_to', 'is_active',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'includes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'One item per line'}),
            'excludes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'One item per line'}),
            'available_from': forms.DateInput(attrs={'type': 'date'}),
            'available_to': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned = super().clean()
        from_date = cleaned.get('available_from')
        to_date = cleaned.get('available_to')
        if from_date and to_date and from_date > to_date:
            raise forms.ValidationError(
                'Available-from date must be before available-to date.',
            )
        return cleaned


class DestinationForm(forms.ModelForm):
    """Staff form for creating/editing destinations."""
    class Meta:
        model = Destination
        fields = ['name', 'country', 'description', 'image', 'featured']
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}


class ReviewForm(forms.ModelForm):
    """Customer review submission after a completed booking."""
    rating = forms.ChoiceField(
        choices=[(i, f'{i} star{"s" if i > 1 else ""}') for i in range(5, 0, -1)],
        widget=forms.Select(),
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Tell other travellers about your experience...',
            }),
        }
