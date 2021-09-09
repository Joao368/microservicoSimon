import json
from datetime import datetime, timedelta
from flask import *
from Crypto.Hash import SHA256
from dpmlainf.database.Es_bank import elasticsearch_work



#class schema_service:


def reformating_graph(device_id, initial_date, final_date):
    parsed_dict = {}
    db = elasticsearch_work()
    response = db.es_time_search(device_id, initial_date, final_date)
    for hit in response["hits"]["hits"]:
        source = hit["_source"]
        source["date"] = datetime \
            .fromtimestamp(source["date"]) \
            .strftime("%d/%m/%Y %H:%M:%S")  # Formatting timestamp to a formatted string literal
        if source["date"] not in parsed_dict:
            parsed_dict.update({source["date"]: {"TEMPERATURA": 0, "UMIDADE": 0}})
        date = source["date"]
        if source["property"] in parsed_dict[date]:
            _property = source["property"]
            parsed_dict[date][_property] = source["value"]

    res_to_return = {"graph_data": []}
    for date in parsed_dict:
        res_to_return["graph_data"].append(
            [date,
             parsed_dict[date]["TEMPERATURA"],
             parsed_dict[date]["UMIDADE"]]
        )

    return res_to_return

def formating_data( device_id, property):
    db = elasticsearch_work()
    response = db.get_last_register(device_id, property)
    _id = response["hits"]["hits"][0]["_id"]
    data = response["hits"]["hits"][0]["_source"]
    data["date"] = datetime \
        .fromtimestamp(data["date"]) \
        .strftime("%d/%m/%Y %H:%M:%S")

    return _id, data

def get_schema(file, index, body):
    _SENSOR_DATA = '/home/joao/Documents/linux dados/worckspace/projSimon/dpmlainf/service/sensor_data.schema'
    _DEVICE = '/home/joao/Documents/linux dados/worckspace/projSimon/dpmlainf/service/device.schema'
    _OPERACIONAL_UNITY = '/home/joao/Documents/linux dados/worckspace/projSimon/dpmlainf/service/operational_unity.schema'
    db = elasticsearch_work()
    if file =="device":
        with open( _DEVICE, 'r') as f:
            schema =  json.loads(f.read())
            return db.send_to_DB(index,body,schema )
    elif file == "operational_unities":
        with open(_OPERACIONAL_UNITY, 'r') as f:
            schema = json.loads(f.read())
            return db.send_to_DB(index,body,schema )
    elif file == "sensor":
        with open(_SENSOR_DATA, 'r') as f:
            schema = json.loads(f.read())
            response= db.send_to_DB(index,schema, body )
            return response


def formating_ID(index,device_id, type):
    res_to_return = {}
    h = SHA256.new()
    db = elasticsearch_work()
    response = db.search_index(index, device_id,)
    if type == "data":
        for hit in response:
            hit_dict = hit.to_dict()
            hit_dict["id"] = hit_dict["id"][5:]  # Formatting ID to remove URI header
            hit_dict["date"] = datetime \
                .fromtimestamp(hit_dict["date"]) \
                .strftime("%d/%m/%Y %H:%M:%S")  # Formatting timestamp to a formatted string literal
            h.update(json.htmlsafe_dumps(res_to_return).encode('utf-8'))  # Calculate the hash to use as key
            res_to_return.update({h.hexdigest(): hit_dict})

            return res_to_return
    else:
        for hit in response:
            hit_dict = hit.to_dict()
            hit_dict["id"] = hit_dict["id"][5:]  # Formatting ID to remove URI header
            h.update(json.htmlsafe_dumps(res_to_return).encode('utf-8'))  # Calculate the hash to use as key
            res_to_return.update({h.hexdigest(): hit_dict})

            return res_to_return