from django import forms

class ShelfForm(forms.Form):
    user_id = forms.CharField(label='User ID', max_length=50)