from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from .models import Candidate, Province, Commune

import json

# Create your views here.

name = { 'miasto': 'city',
         'wies': 'village',
         'zagranica': 'abroad',
         'statek': 'ship',
        }


def wojewodztwo(request):
    if request.method == 'POST':
        province = request.POST.get('nazwa')
        provincepk = Province.objects.filter(name=province)[0].pk
        results = []
        for obj in Commune.objects.filter(province=provincepk):
            data = []
            data.append(obj.name + " " + obj.candidate1.__str__() + ": " + str(obj.candidate1_votes) + " " + obj.candidate2.__str__() + ": " + str(obj.candidate2_votes))
            results.append(data)
        return HttpResponse(json.dumps(results))


def typ(request):
    if request.method == 'POST':
        type = name[request.POST.get('nazwa')]
        results = []
        for obj in Commune.objects.filter(type=type):
            data = []
            data.append(obj.__str__() + " " + obj.candidate1.__str__() + ": " + str(obj.candidate1_votes) + " " + obj.candidate2.__str__() + ": " + str(obj.candidate2_votes))
            results.append(data)
        return HttpResponse(json.dumps(results))


def rozmiar(request):
    if request.method == 'POST':
        type = request.POST.get('nazwa')
        results = []
        if type == 'statki i zagranicza':
            objs = Commune.objects.filter(Q(type='ship') | Q(type='abroad'))
        elif type == "5000":
            objs = Commune.objects.filter(habitancy__lte=type)
        elif type == "500000":
            objs = Commune.objects.filter(habitancy__gt=type)
        else:
            type2 = request.POST.get('nazwa2')
            objs = Commune.objects.filter(habitancy__gte=type, habitancy__lte=type2)
        for obj in objs:
            data = []
            data.append(obj.__str__() + " " + obj.candidate1.__str__() + ": " + str(obj.candidate1_votes) + " " + obj.candidate2.__str__() + ": " + str(obj.candidate2_votes))
            results.append(data)
        return HttpResponse(json.dumps(results))


def votes(request):
    candidates = Candidate.overall()
    results = Province.results()
    types = Commune.types_results()
    sizes = Commune.size_results()
    return render(request, 'wyniki/index.html', {'sizes': sizes, 'candidates': candidates, 'results': results, 'types': types})
