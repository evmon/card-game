import re

from django import forms
from django.core.exceptions import ValidationError


class GameInputForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['player_count'].label = "Number of Players"
        self.fields['square_count'].label = "Number of Squares on the board"
        self.fields['card_count'].label = "Number of Cards in the deck"
        self.fields['colors'].label = "Sequence of characters on the board"
        self.fields['cards'].label = "Cards in the deck"

    player_count = forms.IntegerField(min_value=1, max_value=4)
    square_count = forms.IntegerField(min_value=1, max_value=79)
    card_count = forms.IntegerField(min_value=1, max_value=200)
    colors = forms.CharField()
    cards = forms.CharField()

    def clean_colors(self):
        colors = self.cleaned_data.get('colors')
        if not colors.isalpha():
            raise forms.ValidationError(
                'Sequence of characters on the board must has letters only!')
        if len(colors) != self.cleaned_data.get('square_count'):
            raise forms.ValidationError(
                'Sequence of characters on the board must be equal \
                number of squares on the board!')
        return colors

    def clean_cards(self):
        cards = self.cleaned_data.get('cards')
        card_count = self.cleaned_data.get('card_count')
        cards_split = cards.upper().split(",")

        if len(cards_split) != card_count:
            raise forms.ValidationError(
                'Sequence of characters on the board must be equal \
                number of cards in the deck!')

        for card in cards_split:
            if not card.isalpha():
                # all cards in the deck must be letter value
                raise forms.ValidationError(
                    'Cards in the deck must have letters only!')

            if len(card) > 2:
                # all cards in the deck must have no more than 2 characters
                raise forms.ValidationError(
                    'The card must has less or equal 2 characters!')

            if len(card) == 2 and re.search(r'^(.)\1$', card) == None:
                # raise error, if card in the deck has 2 different characters
                raise forms.ValidationError(
                    'If the card has two characters, they must be the same!')
        return cards
