from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from engine.game.game import Game
from engine.responses.generator_response import GeneratorResponse
from engine.toolkit.constants import *


def index_page(request):
    return render(request, "index.html")


def get_card_file(card, combination):
    return f"{card.rank}-{card.suit}{'-frame' if card in combination.cards else ''}.png"


def generate_mode_page(request, stage = 0):
    response: GeneratorResponse = Game().play()
    template = loader.get_template('generator.html')

    # combination
    current_combination = response.combinations[stage]

    # players_info
    players = response.players
    players_predictions = response.predictions[stage][:-1]
    players_files = [[get_card_file(card, current_combination) for card in player.cards] for player in players]

    # dealer_info
    dealer = [response.dealer]
    dealer_prediction = [response.predictions[stage][-1]]
    dealer_files = [[get_card_file(card, current_combination) for card in response.dealer.cards[:sum(tours[:stage + 1])]]]

    context = {"combination": current_combination,
               "players_info": zip(players, players_predictions, players_files),
               "dealer_info": zip(dealer, dealer_prediction, dealer_files)}

    return HttpResponse(template.render(context, request))
