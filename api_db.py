import boto3
from boto3.dynamodb.conditions import Key, Attr
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import datetime
from flask import Flask, request, redirect, json
import json
from flask_cors import CORS
import logging
import argparse
import random
import os
app = Flask(__name__)
CORS(app)


@app.route("/iot", methods=["POST"])
def iotWrite():
    request_data = request.get_json()
    # request.get_json()
    Device1ID = request_data["Device1ID"]
    # Device1ID = request.args.get('Device1ID')
    # Device1ID = request.form['Device1ID']
    # Device1ID = request_data["Device1ID"]
    # data = request.form["data"]
    # projectName = request.form["projectName"]
    # emailAdress = request.form["emailAdress"]
    # yourName = request.form["yourName"]
    # description = request.form["description"]
    # print(Device1ID)

    # tableHqc.put_item(
    #    Item={
    #         'ID': time.strftime('%Y-%m-%d %H:%M:%S') + '-' + random.randint(1, 10000000),
    #         'Device1ID': Device1ID
    #     }
    # )
    # tablePublish.put_item(
    #    Item={
    #         'clientID': clientID,
    #         'time': time.strftime('%Y-%m-%d %H:%M:%S'),
    #         'yourName': yourName,
    #         'emailAdress': emailAdress,
    #         'projectName': projectName,
    #         'description': description,
    #         'data': data
    #     }
    # )
    response = app.response_class(
        json.dumps({
        'status': 200,
        'text': 'success',
        'Device1ID': Device1ID
        }),
        mimetype='application/json'
    )
    return response

@app.route("/publish", methods=["POST"])
def publish_programming():
    clientID = request.form["clientID"]
    data = request.form["data"]
    projectName = request.form["projectName"]
    emailAdress = request.form["emailAdress"]
    yourName = request.form["yourName"]
    description = request.form["description"]
    print(projectName)
    tablePublish.put_item(
       Item={
            'clientID': clientID,
            'time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'yourName': yourName,
            'emailAdress': emailAdress,
            'projectName': projectName,
            'description': description,
            'data': data
        }
    )
    response = app.response_class(
        json.dumps({
        'status': 200,
        'text': 'success',
        }),
        mimetype='application/json'
    )
    return response

@app.route("/published", methods=["GET"])
def get_all_published():
    response = tablePublish.scan()
    items = response['Items']
    return_data = list()
    for item in items:
        data_dict = dict()
        data_dict["clientID"] = item["clientID"]
        data_dict["time"] = item["time"]
        data_dict["yourName"] = item["yourName"]
        data_dict["emailAdress"] = item["emailAdress"]
        data_dict["projectName"] = item["projectName"]
        data_dict["description"] = item["description"]
        data_dict["data"] = item["data"]
        return_data.append(data_dict)
    result = sorted(return_data, key=lambda k: k['time'], reverse=True)
    return json.dumps(result)

@app.route("/onePublished", methods=["GET"])
def get_one_published():
    request_data = request.args
    clientID = request_data['clientID']
    response = tablePublish.query(
        KeyConditionExpression=Key('clientID').eq(clientID)
    )
    items = response['Items']
    return json.dumps(items[0])

@app.route("/webclient", methods=["GET"])
def get_all_webclient():
    response = table.scan()
    items = response['Items']
    return_data = list()
    timeNow = datetime.datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
    for item in items:
        data_dict = dict()
        data_dict["clientId"] = item["Id"]
        data_dict["Time"] = item["Time"]
        if ((timeNow - datetime.datetime.strptime(item["LastTime"], "%Y-%m-%d %H:%M:%S")).total_seconds() > 5):
            data_dict["WebStatus"] = 'Offline'
        else:
            data_dict["WebStatus"] = item["WebStatus"]
        data_dict["User"] = item["User"]
        data_dict["LastTime"] = item["LastTime"]
        return_data.append(data_dict)
    result = sorted(return_data, key=lambda k: k['Time'], reverse=True)
    return json.dumps(result)

print()
# Get the service resource.
dynamodb = boto3.resource('dynamodb')
# Print out some data about the table.
table = dynamodb.Table('OPARP-Client')
tablePublish = dynamodb.Table('OPARP-publish')
tableHqc = dynamodb.Table('hqc')
if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=80)
