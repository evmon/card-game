from django import forms
from django.core.exceptions import ValidationError


class GameInputForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['player_count'].label = "Number​ of​ Players"
        self.fields['square_count'].label = \
            "Number of​ Squares​ on​ the​ board"
        self.fields['card_count'].label = "Number​ of​ Cards​ in​ the​ deck"
        self.fields['colors'].label = \
            "Sequence​ of​ characters on​ the​ board"
        self.fields['cards'].label = "Cards​ in​ the​ deck"\

    player_count = forms.IntegerField(min_value=1, max_value=4)
    square_count = forms.IntegerField(min_value=1, max_value=79)
    card_count = forms.IntegerField(min_value=1, max_value=200)
    colors = forms.CharField()
    cards = forms.CharField()

    # check all inputs here

    def clean(self):
        cleaned_data = super().clean()
        player_count = cleaned_data.get('player_count')
        square_count = cleaned_data.get('square_count')
        card_count = cleaned_data.get('card_count')
        colors = cleaned_data.get('colors')
        cards = cleaned_data.get('cards')
        # if not player_count and not player_count:
        #     raise forms.ValidationError('You have to write something!')
