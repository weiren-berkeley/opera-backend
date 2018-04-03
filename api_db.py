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


@app.route("/iotData", methods=["GET"])
def iotGet():
    response = tableHqc.scan()
    items = response['Items']
    return_data = list()
    for item in items:
        print(item)
        data_dict = dict()
        # data_dict["Device1ID"] = item["Device1ID"]
        # data_dict["Device1ID"] = item["Device1ID"]
        # data_dict["airTemp"] = item["airTemp"]
        # data_dict["airHumi"] = item["airHumi"]
        # data_dict["Device2ID"] = item["Device2ID"]
        # data_dict["temp2"] = item["temp2"]
        # data_dict["humi2"] = item["humi2"]
        # data_dict["Device3ID"] = item["Device3ID"]
        # data_dict["temp3"] = item["temp3"]
        # data_dict["humi3"] = item["humi3"]
        # data_dict["Device4ID"] = item["Device4ID"]
        # data_dict["temp4"] = item["temp4"]
        # data_dict["humi4"] = item["humi4"]
        # data_dict["Device5ID"] = item["Device5ID"]
        # data_dict["temp5"] = item["temp5"]
        # data_dict["humi5"] = item["humi5"]
        return_data.append(data_dict)
    return json.dumps(return_data)

@app.route("/iot", methods=["POST"])
def iotWrite():
    request_data = request.get_json()
    Device1ID = request_data["Device1ID"]
    airTemp = request_data["airTemp"]
    airHumi = request_data["airHumi"]
    Device2ID = request_data["Device2ID"]
    temp2 = request_data["temp2"]
    humi2 = request_data["humi2"]
    Device3ID = request_data["Device3ID"]
    temp3 = request_data["temp3"]
    humi3 = request_data["humi3"]
    Device4ID = request_data["Device4ID"]
    temp4 = request_data["temp4"]
    humi4 = request_data["humi4"]
    Device5ID = request_data["Device5ID"]
    temp5 = request_data["temp5"]
    humi5 = request_data["humi5"]

    tableHqc.put_item(
       Item={
            'ID': time.strftime('%Y-%m-%d %H:%M:%S') + '-' + str(random.randint(1, 10000000)),
            'Device1ID': Device1ID,
            'airTemp': airTemp,
            'airHumi': airHumi,
            'Device2ID': Device2ID,
            'temp2': temp2,
            'humi2': humi2,
            'Device3ID': Device3ID,
            'temp3': temp3,
            'humi3': humi3,
            'Device4ID': Device4ID,
            'temp4': temp4,
            'humi4': humi4,
            'Device5ID': Device5ID,
            'temp5': temp5,
            'humi5': humi5
        }
    )
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
