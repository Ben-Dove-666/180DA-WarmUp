import paho.mqtt.client as mqtt
from rps import *

#game vars 
player1_val = 0
player2_val = 0
pla1_rece = False
pla2_rece = False


# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))

  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
    client.subscribe("meme/yee1", qos=1)
    client.subscribe('meme/yee2', qos=1)


# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')


# The default message callback.
# (you can create separate callbacks per subscribed topic)
def on_message(client, userdata, message):
    if message.topic == 'meme/yee1': 
        global player1_val 
        player1_val = message.payload
        global pla1_rece
        pla1_rece = True 
    elif message.topic == 'meme/yee2': 
        global player2_val
        player2_val = message.payload 
        global pla2_rece
        pla2_rece = True 
    #print('Received message: "' + str(message.payload) + '" on topic "' +
    #    message.topic + '" with QoS ' + str(message.qos))
    print("player one input: " + str(player1_val)  + "      " 
        + "player two input: " + str(player2_val) )


# 1. create a client instance.
cli_name = "player2"
client = mqtt.Client(cli_name)
# add additional client options (security, certifications, etc.)
# many default options should be good to start off.
# add callbacks to client.
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# 2. connect to a broker using one of the connect*() functions.
# client.connect_async("test.mosquitto.org")
client.connect_async('mqtt.eclipseprojects.io')
# client.connect("test.mosquitto.org", 1883, 60)
# client.connect("mqtt.eclipse.org")

# 3. call one of the loop*() functions to maintain network traffic flow with the broker.
client.loop_start()
# client.loop_forever()

while True:  # perhaps add a stopping condition using some break or something.
      # do your non-blocked other stuff here, like receive IMU data or something.
# use subscribe() to subscribe to a topic and receive messages.
    val = input("Enter a int between 1 and 10: ")
    err, mid = client.publish("meme/yee2",val)
    
    while not pla1_rece or not pla2_rece: 
        pass  #if you had graphics or soething, you would update graphics here.
    
    fight(player1_val, player2_val)
    player1_val = 0
    player2_val = 0
    pla1_rece = False
    pla2_rece = False   

# use publish() to publish messages to the broker.

# use disconnect() to disconnect from the broker.
client.loop_stop()
client.disconnect()