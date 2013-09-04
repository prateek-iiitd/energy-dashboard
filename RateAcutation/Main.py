__author__ = 'prateek'

import httplib
import json

conn = httplib.HTTPConnection("192.168.1.40:9101")

def get_query_response(query):
    conn.request("POST","/api/query",query)
    response = conn.getresponse()
    return response.read()

def get_meter_ids_from_flat(FlatNumber):
    query = "select distinct Metadata/Extra/MeterID where Metadata/Extra/FlatNumber = '%s'" %FlatNumber
    result = get_query_response(query).strip("[]").split(",")
    meters = [x.strip('" ') for x in result]
    return meters

def get_path_from_meter_id(MeterID):
    query = "select distinct Path where Metadata/Extra/MeterID = '%s' and Metadata/Extra/PhysicalParameter = 'Power'" %MeterID
    result = get_query_response(query).strip("[]").split(",")
    power_paths = [x.strip('" ') for x in result]
    return "/data" + power_paths[0][:-5]

def get_meter_type_from_meter_id(MeterID):
    query = "select distinct Metadata/Extra/Type where Metadata/Extra/MeterID = '%s'" %MeterID
    result = get_query_response(query).strip("[]").split(",")
    meter_type = [x.strip('" ') for x in result]
    return meter_type[0]

def get_polling_rate_from_meter_id(MeterID):
    rate_path = get_path_from_meter_id(MeterID) + "Rate"

    query = "select distinct Metadata/Extra/IP where Metadata/Extra/MeterID = '%s'" %MeterID
    result = get_query_response(query).strip("[]").split(",")
    ip = [x.strip('" ') for x in result][0]
    raspi_conn = httplib.HTTPConnection(ip,8080)
    raspi_conn.request("GET",rate_path)
    response = raspi_conn.getresponse()
    results = json.loads(response.read())
    return results['Readings'][0][1]+1

def change_rate_for_meter_id(MeterID, state):
    change_path = get_path_from_meter_id(MeterID) + "Rate?state=%s" %str(state)
    
    query = "select distinct Metadata/Extra/IP where Metadata/Extra/MeterID = '%s'" %MeterID
    result = get_query_response(query).strip("[]").split(",")
    ip = [x.strip('" ') for x in result][0]

    raspi_conn = httplib.HTTPConnection(ip,8080)
    raspi_conn.request("PUT",change_path)
    response = raspi_conn.getresponse()
    if (response.status == 200):
        return True
    else:
        return False

def get_flatnums():
    query = "select distinct Metadata/Extra/FlatNumber where Metadata/Location/Building = 'Faculty Housing' and not Metadata/Extra/FlatNumber='0'"
    result = get_query_response(query).strip("[]").split(",")
    flats = sorted([x.strip('" ') for x in result])
    return flats

def get_meter_id(flatnum, meter_type):
    query = "select distinct Metadata/Extra/MeterID where Metadata/Extra/FlatNumber = '%s' and Metadata/Extra/Type = '%s'" %(flatnum,meter_type)
    result = get_query_response(query)
    ids = [x.strip('" ') for x in result]
    return ids[0]

def meter_types_from_flatnum(flatnum):
    query = "select distinct Metadata/Extra/Type where Metadata/Extra/FlatNumber = '%s'" %flatnum
    results = get_query_response(query)
    meter_types = [x.strip('" ') for x in result]
    return meter_types


# print get_meter_ids_from_flat('101')
# print get_meter_type_from_meter_id('2')
# print get_polling_rate_from_meter_id('2')
# print change_rate_for_meter_id('191','10')
# print change_rate_for_meter_id('191','30')
# print get_flatnums()

