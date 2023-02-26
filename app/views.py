from dataclasses import dataclass

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from engine.game.game import Game
from engine.game.player import Player
from engine.toolkit.combination import Combination
from engine.responses.generator_response import GeneratorResponse
from engine.toolkit.constants import *


@dataclass
class GeneratorContext:
    player: Player
    prediction: int
    combination: Combination
    files: list[str]


def index_page(request):
    return render(request, "index.html")


def get_card_file(card, combination):
    if card is None:
        return "jokers.png"
    return f"{card.rank}-{card.suit}{'-frame' if card in combination.cards else ''}.png"


def generate_mode_page(request, stage = 0):
    response: GeneratorResponse = Game().play()
    template = loader.get_template('generator.html')

    # context
    players_context = list()
    shown_cards = sum(tours[:stage + 1])
    best_combination = response.best_combinations[stage]
    response.players[-1].cards = response.players[-1].cards[:shown_cards] + [None] * (sum(tours) - shown_cards)
    response.players_combinations[stage] += [None]
    for player, prediction, combination in zip(response.players, response.predictions[stage], response.players_combinations[stage]):
        players_context.append(GeneratorContext(player, prediction, combination, [get_card_file(card, best_combination) for card in player.cards]))

    context = {"best_combination": best_combination,
               "players_context": players_context[:-1],
               "dealer_context": players_context[-1:]}

    return HttpResponse(template.render(context, request))
