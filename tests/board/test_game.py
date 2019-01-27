import requests
import pytest

from django.urls import reverse

from board.forms import GameInputForm


@pytest.mark.django_db
class TestGame():
    """Tests for game endpoint.
    get: the form with input fields for game.
    post: finding a winner player.
    """
   
    def test_get_form(self, client):
        """GET / returns the form with input fields for game."""
        response = client.get(reverse('game'))
        content = response.content

        assert response.status_code == 200
        assert '<label for="id_player_count">' in str(content)
        assert '<label for="id_square_count">' in str(content)
        assert '<label for="id_card_count">' in str(content)
        assert '<label for="id_colors">' in str(content)
        assert '<label for="id_cards">' in str(content)


@pytest.mark.parametrize('player_count, square_count, card_count, colors, \
    cards, validity',
    [
        (2, 9, 4, 'AVHFISKSH', 'A,VV,F,S', True),
        (2, 9, 4, 'AVHFISKSH', 'A,VB,F,S', False),
        (5, 9, 4, 'AVHFISKSH', 'A,VV,F,S', False),
        (4, 99, 4, 'AVHFISKSH', 'A,VV,F,S', False),
        (4, 9, 201, 'AVHFISKSH', 'A,VV,F,S', False),
        (4, 9, 4, 'FISKSH', 'A,VV,F,S', False),
        (4, 9, 4, 'AVHFISKSH', 'A, V,F,S', False),
        (4, 9, 4, 'AVHFISKSH', '9,7,34,6', False),
        (4, 9, 4, 'AVHFISKSH', 'A,VV,6,S', False),
        ('test', 'test', 'test', 'AVHFISKSH', 'A,VV,H,S', False),
        ('test', 'test', 'test', '7', 'A,VV,H,S', False),
        ('', '', '', '', '', False),
        (-1, 9, 4, 'AVHFISKSH', 'A,VV,F,S', False),
        (0, 9, 4, 'AVHFISKSH', 'A,VV,F,S', False),
        (1, -9, 4, 'AVHFISKSH', 'A,VV,F,S', False),
        (1, 9, -4, 'AVHFISKSH', 'A,VV,F,S', False),
    ]
)
def test_form_is_valid(player_count, square_count, card_count, colors, cards, validity):
    form = GameInputForm(data={
        'player_count': player_count,
        'square_count': square_count,
        'card_count': card_count,
        'colors': colors,
        'cards': cards,
    })

    assert form.is_valid() is validity
