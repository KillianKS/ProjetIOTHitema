import network
import time
import machine
import dht
from umqtt.simple import MQTTClient

# === CONFIGURATION ===
MQTT_BROKER = "51.38.185.58"
TOPIC_PUBLISH = b"capteurs/kn/data"
TOPIC_ARROSAGE = b"capteurs/arrosage"
ID_CAPTEUR = "capteur_001"
SEUIL_HUMIDITE = 40

# === INIT COMPOSANTS ===
dht_pin = machine.Pin(15)
capteur = dht.DHT22(dht_pin)

servo = machine.PWM(machine.Pin(13), freq=50)

# === FONCTIONS SERVO ===
def ouvrir_vanne():
    servo.duty(120)  # Valeur à ajuster selon servo
    print("💧 Vanne ouverte")

def fermer_vanne():
    servo.duty(40)  # Valeur à ajuster selon servo
    print("🛑 Vanne fermée")

# === MQTT CALLBACK ===
def on_message(topic, msg):
    print(f"📩 MQTT reçu : {topic} - {msg}")
    if topic == TOPIC_ARROSAGE:
        if msg == b"ON":
            ouvrir_vanne()
        elif msg == b"OFF":
            fermer_vanne()

# === CONNEXION WIFI ===
def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect("Wokwi-GUEST", "")  # Réseau Wokwi
    while not wifi.isconnected():
        print(".", end="")
        time.sleep(0.5)
    print("✅ Connecté au Wi-Fi")

# === CONNEXION MQTT ===
def connect_mqtt():
    client = MQTTClient(ID_CAPTEUR, MQTT_BROKER)
    client.set_callback(on_message)
    client.connect()
    client.subscribe(TOPIC_ARROSAGE)
    print(f"✅ Abonné à {TOPIC_ARROSAGE}")
    return client

# === PROGRAMME PRINCIPAL ===
connect_wifi()
mqtt_client = connect_mqtt()

while True:
    mqtt_client.check_msg()  # Écoute des messages

    try:
        capteur.measure()
        temp = capteur.temperature()
        hum = capteur.humidity()

        print(f"🌡 Temp: {temp}°C | 💧 Hum: {hum}%")

        # Envoi des données capteur
        payload = f'{{"id_capteur": "{ID_CAPTEUR}", "temperature": {temp}, "humidite": {hum}}}'
        mqtt_client.publish(TOPIC_PUBLISH, payload)

        # Déclenchement auto de la vanne
        if hum < SEUIL_HUMIDITE:
            mqtt_client.publish(TOPIC_ARROSAGE, b"ON")
        else:
            mqtt_client.publish(TOPIC_ARROSAGE, b"OFF")

    except Exception as e:
        print("❌ Erreur capteur :", e)

    time.sleep(10)




{
  "version": 1,
  "author": "Uri Shaked",
  "editor": "wokwi",
  "parts": [
    { "type": "board-esp32-devkit-c-v4", "id": "esp", "top": -38.4, "left": -91.16, "attrs": {} },
    { "type": "wokwi-dht22", "id": "dht1", "top": -32.2, "left": 40.16, "attrs": {} },
    { "type": "servo", "id": "servo1", "top": 88.8, "left": 47.6, "attrs": {} },
    { "type": "wokwi-servo", "id": "servo2", "top": -174.8, "left": -105.6, "attrs": {} }
  ],
  "connections": [
    [ "esp:TX", "$serialMonitor:RX", "", [] ],
    [ "esp:RX", "$serialMonitor:TX", "", [] ],
    [ "dht1:VCC", "esp:3V3", "red", [ "v109.3", "h-170.36", "v-200.78" ] ],
    [ "dht1:SDA", "esp:15", "green", [ "v0" ] ],
    [ "dht1:GND", "esp:GND.1", "black", [ "v99.7", "h-189.56", "v-66.38" ] ],
    [ "servo1:PWM", "esp:13", "orange", [ "v0" ] ],
    [ "servo1:V+", "esp:3V3", "red", [ "v-30", "h-60", "v-100" ] ],
    [ "servo1:GND", "esp:GND.2", "black", [ "v-10", "h-40", "v-100" ] ],
    [ "servo2:GND", "esp:GND.2", "black", [ "h0" ] ],
    [ "servo2:V+", "esp:3V3", "green", [ "h0" ] ],
    [ "servo2:PWM", "esp:13", "green", [ "h0" ] ]
  ],
  "dependencies": {}
}




import network
import time
import machine
import dht
from umqtt.simple import MQTTClient

# === CONFIGURATION ===
MQTT_BROKER = "51.38.185.58"
TOPIC_PUBLISH = b"capteurs/kn/data"
TOPIC_ARROSAGE = b"capteurs/arrosage"
ID_CAPTEUR = "capteur_001"
SEUIL_HUMIDITE = 40

# === INIT COMPOSANTS ===
dht_pin = machine.Pin(15)
capteur = dht.DHT22(dht_pin)

servo = machine.PWM(machine.Pin(13), freq=50)

# === FONCTIONS SERVO ===
def ouvrir_vanne():
    servo.duty(40)  # Valeur à ajuster selon servo
    print("💧 Vanne ouverte")

def fermer_vanne():
    servo.duty(120)  # Valeur à ajuster selon servo
    print("🛑 Vanne fermée")

# === MQTT CALLBACK ===
def on_message(topic, msg):
    print(f"📩 MQTT reçu : {topic} - {msg}")
    if topic == TOPIC_ARROSAGE:
        if msg == b"ON":
            ouvrir_vanne()
        elif msg == b"OFF":
            fermer_vanne()

# === CONNEXION WIFI ===
def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect("Wokwi-GUEST", "")  # Réseau Wokwi
    while not wifi.isconnected():
        print(".", end="")
        time.sleep(0.5)
    print("✅ Connecté au Wi-Fi")

# === CONNEXION MQTT ===
def connect_mqtt():
    client = MQTTClient(ID_CAPTEUR, MQTT_BROKER)
    client.set_callback(on_message)
    client.connect()
    client.subscribe(TOPIC_ARROSAGE)
    print(f"✅ Abonné à {TOPIC_ARROSAGE}")
    return client

# === PROGRAMME PRINCIPAL ===
connect_wifi()
mqtt_client = connect_mqtt()

while True:
    mqtt_client.check_msg()  # Écoute des messages

    try:
        capteur.measure()
        temp = capteur.temperature()
        hum = capteur.humidity()

        print(f"🌡 Temp: {temp}°C | 💧 Hum: {hum}%")

        # Envoi des données capteur
        payload = f'{{"id_capteur": "{ID_CAPTEUR}", "temperature": {temp}, "humidite": {hum}}}'
        mqtt_client.publish(TOPIC_PUBLISH, payload)

        # Déclenchement auto de la vanne
        if hum < SEUIL_HUMIDITE:
            mqtt_client.publish(TOPIC_ARROSAGE, b"ON")
        else:
            mqtt_client.publish(TOPIC_ARROSAGE, b"OFF")

    except Exception as e:
        print("❌ Erreur capteur :", e)

    time.sleep(10)


{
  "version": 1,
  "author": "Uri Shaked",
  "editor": "wokwi",
  "parts": [
    { "type": "board-esp32-devkit-c-v4", "id": "esp", "top": -38.4, "left": -91.16, "attrs": {} },
    { "type": "wokwi-dht22", "id": "dht1", "top": -32.2, "left": 40.16, "attrs": {} },
    { "type": "servo", "id": "servo1", "top": 88.8, "left": 47.6, "attrs": {} },
    { "type": "wokwi-servo", "id": "servo2", "top": -174.8, "left": -105.6, "attrs": {} }
  ],
  "connections": [
    [ "esp:TX", "$serialMonitor:RX", "", [] ],
    [ "esp:RX", "$serialMonitor:TX", "", [] ],
    [ "dht1:VCC", "esp:3V3", "red", [ "v109.3", "h-170.36", "v-200.78" ] ],
    [ "dht1:SDA", "esp:15", "green", [ "v0" ] ],
    [ "dht1:GND", "esp:GND.1", "black", [ "v99.7", "h-189.56", "v-66.38" ] ],
    [ "servo1:PWM", "esp:13", "orange", [ "v0" ] ],
    [ "servo1:V+", "esp:3V3", "red", [ "v-30", "h-60", "v-100" ] ],
    [ "servo1:GND", "esp:GND.2", "black", [ "v-10", "h-40", "v-100" ] ],
    [ "servo2:GND", "esp:GND.2", "black", [ "h0" ] ],
    [ "servo2:V+", "esp:3V3", "green", [ "h0" ] ],
    [ "servo2:PWM", "esp:13", "green", [ "h0" ] ]
  ],
  "dependencies": {}
}
