import boto3
from boto3.dynamodb.conditions import Key, Attr
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import datetime
from flask import Flask, request, redirect
import json
from flask_cors import CORS
import logging
import argparse
import random
import os
app = Flask(__name__)
CORS(app)

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
            ata_dict["WebStatus"] = 'offline'
        else:
            data_dict["WebStatus"] = item["WebStatus"]
        data_dict["User"] = item["User"]
        data_dict["LastTime"] = item["LastTime"]
        return_data.append(data_dict)
    result = sorted(return_data, key=lambda k: k['Time'], reverse=True)
    return json.dumps(result)



# Get the service resource.
dynamodb = boto3.resource('dynamodb')
# Print out some data about the table.
table = dynamodb.Table('OPARP-Client')

if __name__ == "__main__":
    app.debug = False
    app.run(host='0.0.0.0', port=80)
