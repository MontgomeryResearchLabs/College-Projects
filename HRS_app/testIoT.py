from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import max30102
import hrcalc

m = max30102.MAX30102()
dataHR=[]

host = "yourownurl.iot.us-east-2.amazonaws.com"
certPath = "/home/pi/HRS_app/cert/" #you'll need your own cert folder
clientId = "heart_rate_sesnor"
topic = "sensor"
#topic = "$aws/things/myRPi/shadow/update"


# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials("{}RootCA1.pem".format(certPath), "{}Rpi-private.pem.key".format(certPath), "{}Rpi.pem.crt".format(certPath))

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myAWSIoTMQTTClient.connect()

# Publish to the same topic in a loop forever
i = 0


while True:

    red, ir = m.read_sequential()

    dataHR[i*100:(i+1)*100] = red    # For raw data capturing. Not required!
    hr, hr_valid, spo2, spo2_valid = hrcalc.calc_hr_and_spo2(ir[:100], red[:100])

    print(hr, hr_valid, spo2, spo2_valid)

    messageJson = json.dumps({ "HRvalue": hr, "HRvalid": hr_valid, "SpO2value": spo2, "SpO2valid": spo2_valid})
    myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    print('Published topic %s: %s\n' % (topic, messageJson))
    i += 1
    time.sleep(10)
myAWSIoTMQTTClient.disconnect()


