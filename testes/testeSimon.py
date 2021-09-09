#python -m unittest teste/testeSimon.py
#Vc pode usar o método keys() do docionário pra pegar o valor daquela chave ais aleatória
#teste OU refatoroar teste, pegar leitura(last reads) schema, adiciona informaçao e verifica se ela existe(primeiro verifica se ela existe, depois aciona)
# adicionar temperatura e umidade em pares, PRECISO DE UM DE MOVIMENTO TÁ DANDO ERRO NELE
#colocar os schemas numa pastas de schemas"schema/nomedoschema.schema)
#separar os blueprints do main, criar uma classe pra banco de dados
#https://github.com/paulormnas/server-flask
# search_graph_data?id=inmetro/predio02/diele/lameq/dispositivo_002&startDate=&endDate=
# if len(response["hits"]["hits"]) > 0
# {
#  "id": "id://inmetro/predio02/dmtic/laort",
#  "phone_number": "21453125",
#  "name": "Laboratório de Comunicações Ópticas"}

# {"value": 90,
#  "location": [-22.588484, -43.284468],
#  "date": 1561192101.66541,
#  "sensor_model": "DHT22",
#  "id": "id://inmetro/dmtic/lainf/escritorio/dispositivo_001",
#  "property": "UMIDADE"
# }
#search graf retorno {"1625264751.923084": {
#         "TEMPERATURA": 25,
#         "UMIDADE": 90
#     }
# }
# http://0.0.0.0:8079/search_data?id=inmetro/dmtic/lainf/escritorio/dispositivo_001
import unittest
from dpmlainf import main
import json
from datetime import datetime


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = main.create_app()
#        self.schema = main


    def test_get_device(self):
      respostab={"44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a":
                {"device_model": "Raspberry Pi 3 B+",
                  "device_so": "Raspbian",
                  "id":"inmetro/predio06/dmtic/lainf/escritorio/dispositivo_001",
                  "sensors_software_version": "0.0.1.123"}}


      with self.app.test_client() as cliente:
        req_resposta = cliente.get("/get_devices")
        dadosB= json.loads(req_resposta.data)
        self.assertEqual(dadosB, respostab)

#     def test_schema(self):
#
#         parsed_data ={"device_model": "Raspberry Pi 3 B+",
#                  "device_so": 77777,
#                   "id":"inmetro/predio06/dmtic/lainf/escritorio/dispositivo_001",
#                   "sensors_software_version": "0.0.1.123"}
#         _DEVICE = 'device.schema'
#         schema= json.loads(self.schema(file=_DEVICE))
#         with self.assertRaises(ValidationError):
#             validate(parsed_data, schema)

    def test_get_ou(self):
       ou_esperado = { "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a":
           {"id": "inmetro/predio02/dmtic/laort",
            "name": "Laborat\u00f3rio de Comunica\u00e7\u00f5es \u00d3pticas",
            "phone_number": "21453125"}}

       with self.app.test_client() as cliente:
        ou_resposta = cliente.get("/get_ou?id=//inmetro/predio02/dmtic/laort")
        dadosou = json.loads(ou_resposta.data)
        self.assertEqual(ou_esperado,dadosou)

    def test_get_data(self):
        data_atual= datetime.now()
        data_reformulada = data_atual.strftime("%d/%m/%Y %H:%M:%S")
        data_Umidade={"value": 81,
                     "location": [-22.588484, -43.284468],
                     "date": datetime.now().timestamp(),
                     "sensor_model": "DHT22",
                     "id": "id://inmetro/predio06/dmtic/lainf/escritorio/dispositivo_001",
                     "property": "UMIDADE"}
        data_temperatura={"value": 21,
                     "location": [-22.588484, -43.284468],
                     "date": datetime.now().timestamp(),
                     "sensor_model": "DHT22",
                     "id": "id://inmetro/predio06/dmtic/lainf/escritorio/dispositivo_001",
                     "property": "TEMPERATURA"}
        temperatura_resposta={"value": 21,
                     "location": [-22.588484, -43.284468],
                     "date": data_reformulada,
                     "sensor_model": "DHT22",
                     "id": "id://inmetro/predio06/dmtic/lainf/escritorio/dispositivo_001",
                     "property": "TEMPERATURA"}
        umidade_resposta={"value": 81,
                     "location": [-22.588484, -43.284468],
                     "date": data_reformulada,
                     "sensor_model": "DHT22",
                     "id": "id://inmetro/predio06/dmtic/lainf/escritorio/dispositivo_001",
                     "property": "UMIDADE"}


        with self.app.test_client() as cliente:

            temperatura_json= json.dumps(data_temperatura)
            umidade_json= json.dumps(data_Umidade)
            res_ = cliente.post("/persist_data", data=umidade_json)
            self.assertEqual(res_.status_code, 200)
            res = cliente.post("/persist_data",data=temperatura_json)
            self.assertEqual(res.status_code, 200)
            ambiente_resposta=cliente.get("/search_data?id=inmetro/predio06/dmtic/lainf/escritorio/dispositivo_001")
            dados_ambiente= json.loads(ambiente_resposta.data)
            print(dados_ambiente)
            for hash_key in dados_ambiente.keys():
                if dados_ambiente[hash_key]["property"] == "TEMPERATURA":
                    self.assertEqual(temperatura_resposta , dados_ambiente[hash_key])
                if dados_ambiente[hash_key]["property"] == "UMIDADE":
                    self.assertEqual(umidade_resposta, dados_ambiente[hash_key])

    def test_search_graph_data(self):
        data_graph={"graph_data": [
            ["21/07/2021 13:48:25",
             21, 81]]}

        with self.app.test_client() as cliente:
            re_graph = cliente.get("/search_graph_data?id=inmetro/predio06/dmtic/lainf/escritorio/dispositivo_001&startDate=1626886104000&endDate=1626886105000")
            graph_json = json.loads(re_graph.data)
            self.assertEqual(graph_json, data_graph)



