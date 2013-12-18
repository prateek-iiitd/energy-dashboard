# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotModified,HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from forms import ChooseMetersForm, DownloadDataForm
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from backend import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.messages.api import get_messages
from django.template import RequestContext
import calendar

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')

def error(request):
    """Error view"""
    print request._messages
    messages = get_messages(request)
    return render_to_response('LoginError.html', {'messages': messages},
                              RequestContext(request))


def choose_meters(request):
    f = ChooseMetersForm()

    if request.method == "POST":
        f = ChooseMetersForm(request.POST)
        if f.is_valid():
            cleaned_form = f.cleaned_data
            result = find_matching_meters(cleaned_form)
            print result
            request.session['matching_meters'] = result
            return redirect(matching_meters)

    return render(request, 'ChooseMeters.html', {'form': f})


def matching_meters(request):
    meters = []
    if request.method=="POST":
        f = ChooseMetersForm(request.POST)
        if f.is_valid():
            cleaned_form = f.cleaned_data
            meters = sorted(json.loads(find_matching_meters(cleaned_form)))

        print meters

    return render(request, 'MatchingMeters.html',{'meters':meters})

@csrf_exempt
@login_required()
def polling_rate(request):
    if request.method=="GET":
        meter_rate_path = request.GET.get('Path')[:-5]+'Rate'
        ip_query = "select Metadata/Extra/IP where Path = '%s'" %meter_rate_path
        js_response = json.loads(execute_distinct_query(ip_query))[0]
        ip_addr = js_response['Metadata']['Extra']['IP']

        raspi_conn = httplib.HTTPConnection(ip_addr,8080)
        raspi_conn.request("GET",meter_rate_path)
        response = raspi_conn.getresponse()
        result = json.loads(response.read())
        current_rate =  result['Readings'][0][1]+1
        meter = json.loads(get_metadata(request.GET.get('Path')))[0]

        return render(request, 'MeterRate.html', {'meter':meter, 'current_rate':current_rate, 'rates':[str(x) for x in xrange(1,31)]})

    if request.method=="POST" and request.is_ajax():
        js = json.loads(request.body)
        set_rate = js['Rate']
        change_path = js['Path'][:-5]+'Rate'+ "?state=%s" %str(set_rate)
        print set_rate, change_path

        ip_query = "select Metadata/Extra/IP where Path = '%s'" %js['Path']
        js_response = json.loads(execute_distinct_query(ip_query))[0]
        ip_addr = js_response['Metadata']['Extra']['IP']

        if int(set_rate) in xrange(1,31):
            raspi_conn = httplib.HTTPConnection(ip_addr,8080)
            raspi_conn.request("PUT",change_path)
            response = raspi_conn.getresponse()
            if (response.status == 200):
                return HttpResponse()
            else:
                return HttpResponseNotModified()

@login_required()
def download_options(request):
    f = DownloadDataForm()
    if request.method=="GET":
        meter = json.loads(get_metadata(request.GET.get('Path')))[0]
        meter_path = request.GET.get('Path')[:-5]
        query = "select distinct Metadata/Extra/PhysicalParameter where Path like '%s%%'" %meter_path
        parameters = json.loads(execute_distinct_query(query))
        return render(request,'DownloadOptions.html', {'meter':meter, 'parameters':parameters, 'form':f})

    if request.method=="POST":
        f = DownloadDataForm(request.POST)
        if f.is_valid():
            cleaned_form = f.cleaned_data
            response = get_uuid(cleaned_form['path'],cleaned_form['parameter'])
            uuid = json.loads(response)[0]['uuid']
            start = calendar.timegm(cleaned_form['start_time'].utctimetuple())*1000
            end = calendar.timegm(cleaned_form['end_time'].utctimetuple())*1000
            return redirect("http://nms.iiitd.edu.in:9101/api/data/uuid/c5f8631b-211e-52fc-b9ce-5c763f7729f1?starttime=%s&endtime=%s&format=csv&tags=none&timefmt=iso8601&"%(start,end))
    return render(request,'DownloadOptions.html')

@csrf_exempt
def get_blocks(request):
    if request.is_ajax() and request.method == "POST":
        js = json.loads(request.body)
        building = js['Building']
        result = execute_distinct_query(
            "select distinct Metadata/Extra/Block where Metadata/Location/Building = '%s'" % building)
        blocks = sorted([x.strip().replace('"', "") for x in result.strip("[]").split(',')])
        # blocks = [x.strip('" ') for x in result]
        # print json.dumps(blocks)
        return HttpResponse(json.dumps(blocks))
    else:
        return HttpResponseBadRequest()


@csrf_exempt
def get_wings(request):
    if request.is_ajax() and request.method == "POST":
        js = json.loads(request.body)
        building = js['Building']
        block = js['Block']
        result = execute_distinct_query(
            "select distinct Metadata/Extra/Wing where Metadata/Location/Building = '%s' and Metadata/Extra/Block = '%s'" % (
            building, block))
        wings = sorted([x.strip().replace('"', "") for x in result.strip("[]").split(',')])
        # blocks = [x.strip('" ') for x in result]
        # print json.dumps(blocks)
        return HttpResponse(json.dumps(wings))
    else:
        return HttpResponseBadRequest()


@csrf_exempt
def get_floors(request):
    if request.is_ajax() and request.method == "POST":
        js = json.loads(request.body)
        building = js['Building']
        block = js['Block']
        wing = js['Wing']
        result = execute_distinct_query(
            "select distinct Metadata/Location/Floor where Metadata/Location/Building = '%s' and Metadata/Extra/Block = '%s' and Metadata/Extra/Wing = '%s'" % (
            building, block, wing))
        floors = sorted([int(x.strip().replace('"', "")) for x in result.strip("[]").split(',')])
        floors = [str(x) for x in floors]
        # blocks = [x.strip('" ') for x in result]
        # print json.dumps(blocks)
        return HttpResponse(json.dumps(floors))
    else:
        return HttpResponseBadRequest()