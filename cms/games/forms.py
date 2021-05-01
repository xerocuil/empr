from django import forms

class ScrapeGameForm(forms.Form):
    file_name = forms.CharField(label='File name', max_length=128)