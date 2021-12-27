from flask import Flask, render_template, request,jsonify,json
from flask_mqtt import Mqtt
from paho.mqtt.client import Client
import mysql.connector
from datetime import datetime
import time

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="weather"
)


app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = 'mqtt.flespi.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'tueF5e1B3SeaRzGqjpSNgsP0LtABzAAQSElLGacySewxD2NMgtnmM2aljBNHZdnH'
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 1.0


mqtt = Mqtt(app)

@app.route('/')
def index():
    Temp=data_temphumi[0:2]
    Humi=data_temphumi[2:4]
    return render_template("test.html",temp=Temp,humi=Humi)

    # mycursor = db.cursor()
    # mycursor.execute("SELECT Temp,Humi FROM weather_new ORDER BY id DESC LIMIT 1")
    # data = mycursor.fetchall()
    # return render_template("test.html",temp=data[0][0],humi=data[0][1])


@app.route('/_stuff', methods=['GET'])
def stuff():
#     # mycursor = db.cursor()
#     # mycursor.execute("SELECT Temp,Humi FROM weather_new ORDER BY id DESC LIMIT 1")
#     # data = mycursor.fetchall()
#     # return jsonify(temp=data[0][0],humi=data[0][1])

    Temp=data_temphumi[0:2]
    Humi=data_temphumi[2:4]
    # print(Temp, Humi)
    return jsonify(temp=Temp,humi=Humi)
   
data_temphumi=[]

@app.route('/data', methods=['GET'])
def data():
    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM weather_new ORDER BY id DESC LIMIT 10")
    rows = mycursor.fetchall()
    listdata=[]
    for x in rows:
        dictdata={
            "id":x[0],
            "Time":str(x[1]),
            "Temp":x[2], 
            "Humi":x[3]
        }
        listdata.append(dictdata)
        print(str(x[0]))
    return jsonify(listdata)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('IoT/Forecast')


@mqtt.on_message()
def handle_connect(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(data['topic'])
    print(data['payload'])
   
    data_in = str(data['payload'])
    
    global data_temphumi
    data_temphumi=data_in
    mycursor = db.cursor()
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    mycursor.execute("INSERT INTO weather_new (time, temp, humi) VALUES (%s, %s, %s)", (formatted_date,data_in[0:2] ,data_in[2:4]))
    db.commit()

if __name__ == '__main__':
    app.run(debug=True)


