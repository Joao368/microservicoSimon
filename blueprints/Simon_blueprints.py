from flask import *
from flask_cors import cross_origin
from dpmlainf.service import service
from dpmlainf.database import Es_bank

simon_server_blueprint = Blueprint('simon-server-blueprint', __name__)

@simon_server_blueprint.route('/search_graph_data', methods=['GET'])
@cross_origin(send_wildcard=True)
def search_graph_data():

    device_id = request.args.get("id")
    uri = 'id://' + device_id
    initial_date = request.args.get("startDate")
    Initial_date = float(initial_date[0:len(initial_date) - 3])  # Remove miliseconds digits
    final_date = request.args.get("endDate")
    Final_date = float(final_date[0:len(final_date) - 3])
    response = service.reformating_graph(uri, Initial_date, Final_date)

    return response


@simon_server_blueprint.route('/search_data', methods=['GET'])
@cross_origin()
def search_data():
    device_id = request.args.get('id')
    uri = 'id://' + device_id

    res_to_return = {}
    property_list = ["TEMPERATURA", "UMIDADE", "MOVIMENTO"]
    for _property in property_list:
        _id, data = service.formating_data(uri, _property)
        res_to_return.update({_id: data})

    return res_to_return

@simon_server_blueprint.route('/get_devices', methods=['GET'])
@cross_origin()
def get_devices():

    uri = 'id://'
    response = service.formating_ID("devices",uri,"devices",)
    return response




@simon_server_blueprint.route('/get_ou', methods=['GET'])
@cross_origin()
def get_ou():

    ou_id = request.args.get('id')
    uri = 'id://' + ou_id
    response = service.formating_ID("operational_unities",uri,"operational_unities")
    return response




@simon_server_blueprint.route('/persist_data', methods=['POST'])
def persist_data():

    parsed_data = json.loads(request.data)
    response = service.get_schema("sensor","sensors", parsed_data)
    return response


@simon_server_blueprint.route('/add_device', methods=['POST'])
def add_device():

    parsed_data = json.loads(request.data)
    response = service.get_schema("device","devices", parsed_data)
    return response


@simon_server_blueprint.route('/add_ou', methods=['POST'])
def add_ou():
    parsed_data = json.loads(request.data)
    response = service.get_schema("operational_unities", "operational_unities", parsed_data)
    return response