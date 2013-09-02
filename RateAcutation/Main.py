__author__ = 'prateek'

import httplib

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
    return power_paths[0][:-4]

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
    return response.read()

def change_rate_for_meter_id(MeterID, state):
    change_path = get_path_from_meter_id(MeterID) + "Rate?state=%s" %MeterID
    raspi_conn = httplib.HTTPConnection(ip,8080)
    raspi_conn.request("POST",rate_path)
    response = raspi_conn.getresponse()
    return response.read()


conn = httplib.HTTPConnection("192.168.1.40:9101")
print get_meter_ids_from_flat('101')
print get_meter_type_from_meter_id('2')
print get_polling_rate_from_meter_id('2')
print change_rate_for_meter_id('191','10')
print change_rate_for_meter_id('191','30')
