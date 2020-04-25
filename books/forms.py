from django import forms
from django.core.exceptions import ValidationError

def validate_user_id(value):
    try:
        if int(value) <=0:
            raise ValidationError('Must be positive')

    except:
        raise ValidationError('Not a number')

class UserForm(forms.Form):
    user_id = forms.CharField(max_length=50, 
                            required=True,
                            validators=[validate_user_id])


class ShelfForm(forms.Form):
    def __init__(self, shelf_list, *args, **kwargs):
        super(ShelfForm, self).__init__(*args, **kwargs)
        self.fields['shelfname'] = forms.ChoiceField(label='Shelf name',
                                    choices=[(s,s) for s in shelf_list])

        CHOICES=[(True,'True'),
                (False,'False')]

        self.initial['refresh'] = False
        self.fields['refresh'] = forms.ChoiceField(label='Refresh table?',
                        choices=CHOICES,
                        widget=forms.RadioSelect)
