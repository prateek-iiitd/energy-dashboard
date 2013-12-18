# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from forms import MatchingMetersForm
from backend import *
from django.views.decorators.csrf import csrf_exempt
import json


def match_meters(request):
    f = MatchingMetersForm()

    if request.method == "POST":
        f = MatchingMetersForm(request.POST)
        if f.is_valid():
            cleaned_form = f.cleaned_data
            result = process_form(cleaned_form)

    return render(request, 'MatchMeter.html', {'form': f})

@csrf_exempt
def get_blocks(request):
    if request.is_ajax() and request.method=="POST":
        js = json.loads(request.body)
        building = js['Building']
        result = execute_distinct_query("select distinct Metadata/Extra/Block where Metadata/Location/Building = '%s'" %building)
        blocks = [x.strip().replace('"',"") for x in result.strip("[]").split(',')]
        print blocks
        # blocks = [x.strip('" ') for x in result]
        # print json.dumps(blocks)
        return HttpResponse(json.dumps(blocks))
    else:
        return HttpResponseBadRequest()

