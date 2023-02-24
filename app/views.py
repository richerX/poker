from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from engine.game.game import Game
from engine.responses.generator_response import GeneratorResponse
from engine.toolkit.constants import *


def index_page(request):
    return render(request, "index.html")


def generate_mode_page(request, stage = 0):
    response: GeneratorResponse = Game().play()
    template = loader.get_template('generator.html')
    context = {"players": zip(response.players, response.predictions[stage][:-1]),
               "dealer": response.dealer,
               "dealer_cards": response.dealer.cards[:sum(tours[:stage + 1])],
               "dealer_prediction": response.predictions[stage][-1]}
    return HttpResponse(template.render(context, request))
