from copy import deepcopy
from dataclasses import dataclass

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from engine.game.game import Game
from engine.game.player import Player
from engine.toolkit.combination import Combination
from engine.responses.generator_response import GeneratorResponse
from engine.toolkit.constants import *


total_response: GeneratorResponse = None


@dataclass
class GeneratorContext:
    player: Player
    prediction: int
    combination: Combination
    files: list[str]


def get_card_file(card, combination):
    if card is None:
        return "jokers.png"
    return f"{card.rank}-{card.suit}{'-frame' if card in combination.cards else ''}.png"


def index_page(request):
    return render(request, "index.html")


def generate_mode_page(request, stage = 0):
    global total_response
    template = loader.get_template('generator.html')

    # request
    if request.POST.get('prev'):
        stage = int(request.POST.get('stage')) - 1
    elif request.POST.get('next'):
        stage = int(request.POST.get('stage')) + 1
    if stage == 3 or (not request.POST.get('next') and not request.POST.get('prev')):
        total_response = Game().play()
        stage = 0
    stage = max(min(stage, len(tours) - 1), 0)
    response: GeneratorResponse = deepcopy(total_response)

    # context
    players_context = list()
    shown_cards = sum(tours[:stage + 1])
    best_combination = response.best_combinations[stage]
    response.players[-1].cards = response.players[-1].cards[:shown_cards] + [None] * (sum(tours) - shown_cards)
    response.players_combinations[stage] += [None]
    for player, prediction, combination in zip(response.players, response.predictions[stage], response.players_combinations[stage]):
        players_context.append(GeneratorContext(player, prediction, combination, [get_card_file(card, best_combination) for card in player.cards]))

    context = {"stage": stage,
               "players_context": players_context[:-1],
               "dealer_context": players_context[-1:]}

    return HttpResponse(template.render(context, request))


def test_page(request, current = 1):
    template = loader.get_template('test.html')

    if request.POST.get('prev'):
        current = int(request.POST.get('current')) - 1
    elif request.POST.get('next'):
        current = int(request.POST.get('current')) + 1

    context = {"current": current}

    return HttpResponse(template.render(context, request))
