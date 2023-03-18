import json
import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from engine.game.game import Game
from engine.game.deck import Deck
from engine.toolkit.predictor import Predictor
from engine.toolkit.card import Card
from engine.vision.detector import Detector

RANK_MAPPING = {"1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", "10": "10", "J": "11", "Q": "12", "K": "13", "A": "14"}
SUIT_MAPPING = {"s": "spades", "c": "clubs", "d": "diamonds", "h": "hearts"}
Detector.pretrained_model_v5 = "engine/vision/v5.pt"
Detector.pretrained_model_v8 = "engine/vision/v8.pt"
DETECTOR = Detector()


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


def visor_analyze_image(request):
    file = request.FILES["uploaded_file"]
    path = default_storage.save(f"tmp/{file.name}", ContentFile(file.read()))
    detector_data = DETECTOR.detect(os.path.join(settings.MEDIA_ROOT, path))

    response_data = dict()
    for key, value in detector_data.items():
        response_data[f"{RANK_MAPPING[key[:-1]]}-{SUIT_MAPPING[key[-1]]}.png"] = int(value * 100)
    return JsonResponse(response_data)
