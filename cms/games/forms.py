from django import forms
from django.forms import CheckboxInput, FileInput, HiddenInput, Select, SelectMultiple, Textarea, TextInput
from django.utils.translation import gettext_lazy as _

from .models import Game

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = '__all__'
        widgets = {
            'title': TextInput(attrs={
                'required': True,
            }),
            'tags': SelectMultiple(attrs={'size': '8'})
        }