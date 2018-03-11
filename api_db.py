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
        if ((datetime.datetime.strptime(item["LastTime"], "%Y-%m-%d %H:%M:%S") - timeNow).total_seconds() > 5):
            ata_dict["WebStatus"] = 'offline'
        else:
            data_dict["WebStatus"] = item["WebStatus"]
        data_dict["User"] = item["User"]
        data_dict["LastTime"] = item["LastTime"]
        return_data.append(data_dict)
    result = sorted(return_data, key=lambda k: k['Time'], reverse=True)
    return json.dumps(result)
# Custom MQTT message callback
def customCallback(client, userdata, message):
    # print("Received a new message " + "from topic: " + message.topic)
    obj = json.loads(message.payload)
    print(message.payload)
    # print(obj['text'])
    if (obj['type'] == 'status' and 'Id'in obj):
        # print(obj['status'])
        # print(obj['Id'])
        a = datetime.datetime.strptime('2018-03-11 06:00:00', "%Y-%m-%d %H:%M:%S")
        b = datetime.datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
        # print((b-a).total_seconds())
        response = table.query(
            KeyConditionExpression=Key('Id').eq(obj['Id'])
        )
        items = response['Items']
        if (items == []):
            table.put_item(
               Item={
                    'Id': obj['Id'],
                    'Time': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'WebStatus': obj['WebStatus'],
                    'User': obj['Id'],
                    'LastTime': time.strftime('%Y-%m-%d %H:%M:%S')
                }
            )
        else:
            table.update_item(
                Key={
                    'Id': obj['Id'],
                    'Time': items[0]['Time']
                },
                UpdateExpression='SET WebStatus = :val1, LastTime = :val2',
                ExpressionAttributeValues={
                    ':val1': obj['WebStatus'],
                    ':val2': time.strftime('%Y-%m-%d %H:%M:%S')
                }
            )
# print("--------------")
# IoT Seetings


# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Create the DynamoDB table.
# table = dynamodb.create_table(
#     TableName='OPARP-Client',
#     KeySchema=[
#         {
#             'AttributeName': 'Id',
#             'KeyType': 'HASH'
#         },
#         {
#             'AttributeName': 'Time',
#             'KeyType': 'RANGE'
#         }
#     ],
#     AttributeDefinitions=[
#         {
#             'AttributeName': 'Id',
#             'AttributeType': 'S'
#         },
#         {
#             'AttributeName': 'Time',
#             'AttributeType': 'S'
#         }
#     ],
#     ProvisionedThroughput={
#         'ReadCapacityUnits': 5,
#         'WriteCapacityUnits': 5
#     }
# )

# Wait until the table exists.
# table.meta.client.get_waiter('table_exists').wait(TableName='OPARP-Client')

# Print out some data about the table.
table = dynamodb.Table('OPARP-Client')
# table.put_item(
#    Item={
#         'Id': 'oparp001',
#         'Time': time.strftime('%Y-%m-%d %H:%M:%S'),
#         'Status': 'Online',
#         'User': 'weiren',
#     }
# )

host = 'a21zozqgendyv9.iot.us-east-2.amazonaws.com'
rootCAPath = 'root-CA.crt'
certificatePath = 'certificate.pem.crt'
privateKeyPath = 'private.pem.key'
useWebsocket = False
clientId = 'Server' + str(int(random.random()*10000000000000))
print('clintId: ' + clientId)
topic = 'oparp'
mode = 'both'

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
time.sleep(2)
# while(1):
#     time.sleep(2)
if __name__ == "__main__":
    app.debug = False
    app.run(host='0.0.0.0', port=80)
