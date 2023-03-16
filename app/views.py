from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from engine.game.game import Game


def index_page(request):
    return render(request, "index.html")


def generator_page(request):
    template = loader.get_template('generator.html')
    context = {"stages": Game(players = 3).play().get_context()}
    return HttpResponse(template.render(context, request))


def predictor_page(request):
    return render(request, "predictor.html")


def visor_page(request, current = 1):
    template = loader.get_template('visor.html')

    if request.POST.get('prev'):
        current = int(request.POST.get('current')) - 1
    elif request.POST.get('next'):
        current = int(request.POST.get('current')) + 1

    context = {"current": current}

    return HttpResponse(template.render(context, request))
