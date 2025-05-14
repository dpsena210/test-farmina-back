
from flask import request as flask_request

import requests


from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources=r'*')


@app.route('/api/products', methods=['POST'])
def get_data():
    data = flask_request.get_json()
    type = data.get('type')
    gestation = data.get('gestation')
    lactation = data.get('lactation')
    productType = data.get('productType')
    specialcares = data.get('specialcares')
    lifestage = data.get('lifeStage')

    if specialcares != None:
        specialcares_ids =[specialcares]
    else:
        specialcares_ids = []

    result = requests.post("https://gw-c.petgenius.info/wfservice/z1/nutritionalplans/products/list",
                  json={
                      "country": "IT",
                      "countryId": "brand",
                      "type": type,
                      "gestation": bool(gestation),
                      "lactation": bool(lactation),
                      "productType":productType,
                      "specialcares": specialcares_ids,
                      "lifeStage":lifestage
                  },
                  auth=("wsfarmina_zendesk", "test"),
                headers={'Accept': 'application/json'}
                  )

    json_result = result.json()
    results = json_result.get("result")
    products = results["products"]
    if len(products)==0:
        return jsonify({"error":"does not exist"})
    keylist= list(products.keys())
    list_objects = []
    new_object = {}
    for key in keylist:
        new_object["id"] = str(key)
        new_object["type"] = products[key]["type"]
        new_object["name"]= products[key]["name"]
        new_object["productType"]= products[key]["productType"]
        new_object["gestation"]= gestation
        new_object["lactation"]= lactation
        new_object["lifeStages"]= products[key]["lifeStages"]
        new_object["specialcares"]= products[key]["specialcares"]
        list_objects.append(new_object)
        new_object= {}
    return jsonify({"products_filtered":list_objects}),200


@app.route('/api/special', methods=['POST'])
def get_data_specia():
    data = flask_request.get_json()
    type = data.get('type')
    if type is None:
        type = "dog"

    result = requests.post(
        "https://gw-c.petgenius.info/wfservice/z1/specialcares/list",
        json={
            "species":type,
            "country": "IT",
            "type": "dietetic"
        }
        ,
        auth=("wsfarmina_zendesk", "test")
    )

    special_cares = result.json().get("result")[0].get("specialcares")[0].get("list")
    return jsonify({"special_filtered":special_cares}),200


if __name__ == '__main__':
    app.run(debug=True)