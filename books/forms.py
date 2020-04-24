from django import forms
from django.core.exceptions import ValidationError

class UserForm(forms.Form):
    user_id = forms.CharField(max_length=50, required=True)

class ShelfForm(forms.Form):
    def __init__(self, shelf_list, *args, **kwargs):
        super(ShelfForm, self).__init__(*args, **kwargs)
        self.fields['shelfname'] = forms.ChoiceField(label='Shelf name',
                                    choices=[(s,s) for s in shelf_list])
