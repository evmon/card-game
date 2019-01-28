import requests
import pytest

from django.urls import reverse

from board.forms import GameInputForm
from board.models import GameResult


class EqualsInteger:
    """Helper to check that the value compare to is integer.

    For example,

    def test_compare_dicts():
        assert {
            'userName':'bob',
            'id': 2004
        } == {
            'userName': 'bob',
            'lastModified': EqualsInteger()
        }
    """
    def __eq__(self, other):
        return type(other) == int


@pytest.mark.django_db
class TestGame():
    """Tests for game endpoint.
    GET: the form with input fields for game.
    POST: determine the winner player.
    Input parapeters:
        player_count: Number of Players,
        square_count: Number of Squares on the board,
        card_count: Number of Cards in the deck,
        colors: Sequence of characters on the board,
        cards: Cards in the deck.
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

    def test_save_game_result(self, client):
        """POST / returns game result and checked GameResult object.
        The GameResult objects should be created.
        """
        assert GameResult.objects.all().count() == 0
        data = {
            'player_count': 2,
            'square_count': 13,
            'card_count': 8,
            'colors': "RYGPBRYGBRPOP",
            'cards': "R,B,GG,Y,P,B,P,RR"
        }
        response = client.post(reverse('game'), data=data)
        assert GameResult.objects.all().count() == 1
        msg = "Player 1 won after 7 cards."
        expected_result_data = {
            'message': msg,
        }
        assert GameResult.objects.first().info == msg
        assert GameResult.objects.first().id == EqualsInteger()
        assert response.json() == expected_result_data
        data = {
            'player_count': 4,
            'square_count': 13,
            'card_count': 8,
            'colors': "RYGPBRYGBRPOP",
            'cards': "R,B,GG,Y,P,B,P,RR"
        }
        response = client.post(reverse('game'), data=data)
        assert GameResult.objects.all().count() == 2
        msg = "No player won after 8 cards."
        expected_result_data = {
            'message': msg,
        }
        assert response.json() == expected_result_data
        assert GameResult.objects.first().info == msg
        assert GameResult.objects.first().id == EqualsInteger()

    def test_get_game_result_1(self, client):
        """POST / returns game result.
        Input parapeters:
            player_count: 2,
            square_count: 13,
            card_count: 8,
            colors: "RYGPBRYGBRPOP",
            cards: "R,B,GG,Y,P,B,P,RR".
        """
        data = {
            'player_count': 2,
            'square_count': 13,
            'card_count': 8,
            'colors': "RYGPBRYGBRPOP",
            'cards': "R,B,GG,Y,P,B,P,RR"
        }
        response = client.post(reverse('game'), data=data)

        expected_result_data = {
            'message': "Player 1 won after 7 cards.",
        }
        assert response.json() == expected_result_data

    def test_get_game_result_2(self, client):
        """POST / returns game result.
        Input parapeters:
            player_count: 4,
            square_count: 13,
            card_count: 8,
            colors: "RYGPBRYGBRPOP",
            cards: "R,B,GG,Y,P,B,P,RR".
        """
        data = {
            'player_count': 4,
            'square_count': 13,
            'card_count': 8,
            'colors': "RYGPBRYGBRPOP",
            'cards': "R,B,GG,Y,P,B,P,RR"
        }
        response = client.post(reverse('game'), data=data)

        expected_result_data = {
            'message': "No player won after 8 cards.",
        }
        assert response.json() == expected_result_data

    def test_get_game_result_3(self, client):
        """POST / returns game result.
        Input parapeters:
            player_count: 3,
            square_count: 13,
            card_count: 8,
            colors: "RYGPBRYGBRPOP",
            cards: "R,B,GG,Y,P,B,P,RR".
        """
        data = {
            'player_count': 3,
            'square_count': 13,
            'card_count': 8,
            'colors': "RYGPBRYGBRPOP",
            'cards': "R,B,GG,Y,P,B,P,RR"
        }
        response = client.post(reverse('game'), data=data)

        expected_result_data = {
            'message': "Player 2 won after 8 cards.",
        }
        assert response.json() == expected_result_data

    def test_get_game_result_4(self, client):
        """POST / returns game result.
        Input parapeters:
            player_count: 2,
            square_count: 6,
            card_count: 5,
            colors: "RYGRYB",
            cards: "R,YY,G,G".
        """
        data = {
            'player_count': 2,
            'square_count': 6,
            'card_count': 5,
            'colors': "RYGRYB",
            'cards': "R,YY,G,G,B",
        }
        response = client.post(reverse('game'), data=data)
        expected_result_data = {
            'message': "Player 2 won after 4 cards.",
        }
        assert response.json() == expected_result_data

    def test_get_game_result_5(self, client):
        """POST / returns game result.
        Input parapeters:
            player_count: 3,
            square_count: 9,
            card_count: 6,
            colors: "QQQQQQQQQ",
            cards: "Q,QQ,Q,Q,QQ,Q".
        """
        data = {
            'player_count': 3,
            'square_count': 9,
            'card_count': 6,
            'colors': "QQQQQQQQQ",
            'cards': "Q,QQ,Q,Q,QQ,Q",
        }
        response = client.post(reverse('game'), data=data)
        expected_result_data = {
            'message': "No player won after 6 cards.",
        }
        assert response.json() == expected_result_data

    def test_get_game_result_6(self, client):
        """POST / returns game result."""
        data = {
            'player_count': 3,
            'square_count': 79,
            'card_count': 10,
            'colors': "ABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXYABCD",
            'cards': "D,BB,CC,E,A,BB,EE,DD,CC,AA",
        }
        response = client.post(reverse('game'), data=data)
        expected_result_data = {
            'message': "Player 2 won after 8 cards.",
        }
        assert response.json() == expected_result_data

    def test_get_game_result_7(self, client):
        """POST / returns game result."""
        data = {
            'player_count': 1,
            'square_count': 10,
            'card_count': 5,
            'colors': "ABCDEABCDE",
            'cards': "A,B,A,BB,E",
        }
        response = client.post(reverse('game'), data=data)
        expected_result_data = {
            'message': "Player 1 won after 4 cards.",
        }
        assert response.json() == expected_result_data

    def test_get_game_result_8(self, client):
        """POST / returns game result."""
        data = {
            'player_count': 4,
            'square_count': 1,
            'card_count': 1,
            'colors': "Z",
            'cards': "X",
        }
        response = client.post(reverse('game'), data=data)
        expected_result_data = {
            'message': "Player 1 won after 1 cards.",
        }
        assert response.json() == expected_result_data

    def test_get_game_result_9(self, client):
        """POST / returns game result."""
        data = {
            'player_count': 2,
            'square_count': 2,
            'card_count': 2,
            'colors': "AV",
            'cards': "AA,B",
        }
        response = client.post(reverse('game'), data=data)
        expected_result_data = {
            'message': "Player 1 won after 1 cards.",
        }
        assert response.json() == expected_result_data


@pytest.mark.parametrize('player_count, square_count, card_count, colors, \
    cards, validity',
    [
        (2, 9, 4, 'AVHFISKSH', 'A,VV,F,S', True),
        (2, 9, 4, 'AVHFIghSH', 'A,VV,F,S', True),
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
