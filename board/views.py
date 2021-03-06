from django.shortcuts import render
from django.http import JsonResponse

from .forms import GameInputForm
from .models import GameResult


class PlayerInfo():
    # current information about player
    piece = 0


def create_game_result(result):
    # game resuld save to the database
    GameResult.objects.create(info=result)


def response_message(status, *args, **kwargs):
    if status:
        [player, total_cards] = args
        msg = "Player {} won after {} cards.".format(player + 1, total_cards)
        create_game_result(msg)
        return JsonResponse({'message': msg})
    else:
        [total_cards] = args
        msg = "No player won after {} cards.".format(total_cards)
        create_game_result(msg)
        return JsonResponse({'message': msg})


def game(request):
    """View for game endpoint.
    GET: the form with input fields for game.
    POST: determine the winner player.
    Input parapeters:
        player_count: Number of Players,
        square_count: Number of Squares on the board(is not used  in view),
        card_count: Number of Cards in the deck(is not used in view),
        colors: Sequence of characters on the board,
        cards: Cards in the deck,
        total_cards: the total number of cards drawn.
    """
    if request.method == 'POST':
        form = GameInputForm(request.POST)

        if form.is_valid():
            # play game
            player_count = int(request.POST['player_count'])
            colors = request.POST['colors'].upper()
            cards = request.POST['cards'].upper().split(",")
            last_square = colors.rfind(colors[-1]) # index of last square
            player_info = []
            total_cards = 0 # initial number of cards drawn
            player = 0 # player with number 1 goes first

            for key in range(player_count):
                info = PlayerInfo()
                player_info.insert(key, info)

            for index_card, card in enumerate(cards):

                total_cards = total_cards + 1
                if player == player_count: player = 0
                symbol_count = card.count(card[0])

                # if first characters in card and color 
                # in the current board doesn't exist
                if not (card[0] in colors[player_info[player].piece:]):
                    return response_message(True, player, total_cards)
                for index_color, color in enumerate(colors):
                    if (index_color >= player_info[player].piece and
                        color == card[symbol_count-1]):
                        if index_color == last_square:
                            return response_message(
                                True, player, total_cards)
                        else:
                            player_info[player].piece = index_color + 1
                            symbol_count = symbol_count - 1
                            if symbol_count != 0:
                                # if first characters in card and color
                                # in the updated board doesn't exist
                                if not (card[0] in colors[index_color + 1:]):
                                    return response_message(
                                        True, player, total_cards)
                            else: break
                # move to the next player
                player = player + 1
            else:
                return response_message(False, total_cards)
    else:
        form = GameInputForm()
    return render(request, 'board/form.html', {'form': form})
