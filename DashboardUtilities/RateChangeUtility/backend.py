__author__ = 'prateek'
from models import Building
import httplib


# def find_matching_meters(cleaned_form):
#     building = cleaned_form['building']
#     block = cleaned_form['block']
#     floor = cleaned_form['floor']
#     wing = cleaned_form['wing']
#
#     query = "select distinct Path where Metadata/Location/Building = '%s' and Metadata/Location/Floor = '%s' and Metadata/Extra/Block = '%s' and Metadata/Extra/Wing = '%s' and Metadata/Extra/PhysicalParameter = 'Power'" %(building,floor,block,wing)
#     result = execute_distinct_query(query)
#     meter_paths = sorted([x.strip().replace('"', "") for x in result.strip("[]").split(',')])
#     return meter_paths


def execute_distinct_query(query):
    return execute_query(query)

def execute_query(query):
    conn = httplib.HTTPConnection("nms.iiitd.edu.in:9101")
    conn.request("POST","/api/query",query)
    response = conn.getresponse()
    return response.read()

def find_matching_meters(cleaned_form):
    building = cleaned_form['building']
    block = cleaned_form['block']
    floor = cleaned_form['floor']
    wing = cleaned_form['wing']
    query = "select Path, Metadata/Location/Building, Metadata/Location/Floor, Metadata/Extra/MeterID, Metadata/Extra/LoadType, Metadata/Extra/SubLoadType, Metadata/Extra/SupplyType where Metadata/Location/Building = '%s' and Metadata/Location/Floor = '%s' and Metadata/Extra/Block = '%s' and Metadata/Extra/Wing = '%s' and Metadata/Extra/PhysicalParameter = 'Power'" %(building,floor,block,wing)
    return execute_query(query)

def get_metadata(path):
    query = "select Path, Metadata/Location/Building, Metadata/Location/Floor, Metadata/Extra/MeterID, Metadata/Extra/LoadType, Metadata/Extra/SubLoadType, Metadata/Extra/SupplyType where Path = '%s'" %path
    return execute_query(query)


def get_uuid(path, parameter):
    query = "select uuid where Path = '%s'" %(path[:-5]+parameter)
    return execute_distinct_query(query)