import json
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from engine.game.game import Game
from engine.game.deck import Deck
from engine.toolkit.predictor import Predictor
from engine.toolkit.card import Card


def index_page(request):
    return render(request, "index.html")


def generator_page(request):
    template = loader.get_template('generator.html')
    context = {"stages": Game(players = 3).play().get_context()}
    return HttpResponse(template.render(context, request))


def predictor_page(request):
    return render(request, "predictor.html")


def predictor_get_predictions(request):
    deck: Deck = Deck()
    dealer: list[Card] = []
    players: list[list[Card]] = []

    for key, value in json.loads(request.POST["object"]).items():
        if not value[0] or not value[1]:
            continue

        card = Card(int(value[0]), value[1])
        if card not in deck.cards:
            return HttpResponse(f"You entered repeated card - {card}")
        deck.remove(card)

        if key.startswith("dealer"):
            dealer.append(card)
            continue

        index = int(key.split("-")[0].strip("player"))
        while len(players) < index:
            players.append(list())
        players[index - 1].append(card)

    return HttpResponse(";".join(map(lambda x: str(x), Predictor(deck.cards, dealer, players).chances)))


def visor_page(request, current = 1):
    template = loader.get_template('visor.html')

    if request.POST.get('prev'):
        current = int(request.POST.get('current')) - 1
    elif request.POST.get('next'):
        current = int(request.POST.get('current')) + 1

    context = {"current": current}

    return HttpResponse(template.render(context, request))
