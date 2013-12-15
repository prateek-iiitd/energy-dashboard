__author__ = 'prateek'
from models import Building
import httplib


def process_form(cleaned_form):
    building_name = cleaned_form['building']
    block = cleaned_form['block']
    floor = cleaned_form['floor']
    wing = cleaned_form['wing']
    building = Building.objects.get(name=building_name)
    print building.where_clause

    query = "select Path, Metadata/Extra/MeterID, Metadata/Extra/Type, Metadata/Extra/FlatNumber where Path like '%%/Rate' and Metadata/Location/Floor='%s' and Metadata/Extra/Wing='%s' and Metadata/Extra/Block='%s' and %s" % (
        floor, wing, block, building.where_clause)


def execute_distinct_query(query):
    conn = httplib.HTTPConnection("192.168.1.40:9101")
    conn.request("POST","/api/query",query)
    response = conn.getresponse()
    return response.read()