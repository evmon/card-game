from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import FormView

from .forms import GameInputForm
from .models import GameResult


def game(request):
    if request.method == 'POST':
        form = GameInputForm(request.POST)
        # {'csrfmiddlewaretoken': ['3LXUeipFV8BjRweZjijDLd0HhgiKBPXbzwjH2qJ9Pn2GHOJm6x3607Ui48dJzDff'], 
        # 'player_count': ['2'], 'square_count': ['34'], 'card_count': ['12'], 'colors': 
        # ['BAHDIDH'], 'cards': ['k,s,f,g,s,r']}
        if form.is_valid():
            # play game
            # create GameResult object after game is gone
            print(request.POST)
            responseData = {
                'id': 4,
                'name': 'Test Response',
                'roles' : ['Admin','User']
            }

            return JsonResponse(responseData)

    else:
        form = GameInputForm()
        # print(form.player_count)
    return render(request, 'board/form.html', {'form': form})
