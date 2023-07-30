from django import forms
from .models import Recipe


class RecipeCreateForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Recipe Title'}),
        required=True)
    description = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Description'}),
        required=True)
    ingredients = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control form-control-user',
                                     'placeholder': 'Ingredients', 'style': 'height: 80px'}),
        required=True)
    instructions = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control form-control-user',
                                     'placeholder': 'Instructions', 'style': 'height: 80px'}),
        required=True)
    category = forms.TypedChoiceField(
        choices=Recipe.CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        coerce=str,
        required=True)

    picture = forms.ImageField(label='Recipe Picture:')

    class Meta:
        model = Recipe
        fields = ('title', 'ingredients', 'instructions', 'category', 'picture', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['picture'].widget.attrs.update({'enctype': 'multipart/form-data'})