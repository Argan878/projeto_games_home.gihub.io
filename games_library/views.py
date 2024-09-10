from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .models import Game

# View para listar todos os jogos
def home(request):
    games = Game.objects.all()
    return render(request, 'home.html', {'games': games})

def game_list(request):
    games = Game.objects.all()
    return render(request, 'game_list.html', {'games': games})

def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'game_detail.html', {'game': game})

