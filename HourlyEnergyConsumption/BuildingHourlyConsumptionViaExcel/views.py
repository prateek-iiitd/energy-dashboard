# Create your views here.
from django.core.servers.basehttp import FileWrapper
from forms import FileRequestForm
from django.http import HttpResponse
from django.shortcuts import render
from models import Building
from datetime import timedelta
import os
import xlwt
import httplib
import json

def generate_query(building_name, start_time, end_time):
    start = start_time.strftime("%m/%d/%Y %H:%M")
    end_time = end_time + timedelta(days=1, hours=1)
    end = end_time.strftime("%m/%d/%Y %H:%M")
    building = Building.objects.get(pk = building_name)

    query =  "apply window(first, field = 'hour', width=1) to data in ('%s','%s' ) where %s and Metadata/Extra/Type = 'Building Total Mains' and Metadata/Extra/PhysicalParameter = 'Energy'" % (start, end, building.where_clause)
    # print query
    return query

def populate_sheet(sheet,building_name, start_time, end_time):
    conn = httplib.HTTPConnection("192.168.1.40:9101")
    conn.request("POST", "/api/query/", generate_query(building_name,start_time,end_time))
    response = conn.getresponse()
    results = response.read().strip()[1:-1]
    results = json.loads()
    readings = results['Readings']

def process_form(form):
    building_name = form.cleaned_data['building'].name
    start_time = form.cleaned_data['start_time']
    end_time = form.cleaned_data['end_time']

    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet(str(building_name))
    populate_sheet(sheet, building_name,start_time,end_time)

    path = "/home/prateek/Excel/Results.xls"
    book.save(path)
    return path


def home(request):
    if request.method == 'POST':
        form = FileRequestForm(request.POST, request)

        if form.is_valid():
            inst = form.save(commit=False)
            inst.request_IP = request.META['REMOTE_ADDR']
            inst.save()

            abs_path = process_form(form)
            wrapper = FileWrapper(open(abs_path))
            response = HttpResponse(wrapper, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=%s.xls' % 'Results'
            response['Content-Length'] = os.path.getsize(abs_path)

            return response

    else:
        form = FileRequestForm(
            initial={'start_time': '2013-01-01', 'end_time': '2013-01-02', 'building': Building.objects.get(pk='Faculty Housing')})
        return render(request, 'RequestFileForm.html', {'form': form})