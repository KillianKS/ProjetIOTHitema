import paho.mqtt.client as mqtt
import json
import threading
import uuid
from copy import deepcopy

seen_ids = set()
DATA_FILE = "capteurs_data.json"
lock = threading.Lock()

def save_data(data, filename=DATA_FILE):
    lock.acquire()
    try:
        try:
            with open(filename, "r") as f:
                existing = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing = []

        found = False
        for i, d in enumerate(existing):
            if d.get("message_id") == data.get("message_id"):
                existing[i] = data
                found = True
                break
        if not found:
            existing.append(data)

        with open(filename, "w") as f:
            json.dump(existing, f, indent=2)
    finally:
        lock.release()


# Fonction pour simuler plusieurs capteurs à partir d’un seul message
def simulate_multiple_sensors(base_data):
    simulated = []

    capteurs = [
        {"id": "temp_1", "pos": "serre_nord"},
        {"id": "temp_2", "pos": "serre_sud"},
        {"id": "humid_1", "pos": "serre_est"},
        {"id": "humid_2", "pos": "serre_ouest"}
    ]

    for cap in capteurs:
        data = deepcopy(base_data)
        data["id_capteur"] = cap["id"]
        data["position"] = cap["pos"]
        data["message_id"] = str(uuid.uuid4())  # message unique
        simulated.append(data)

    return simulated


def on_message(client, userdata, msg):
    print(f"\n📩 Message reçu sur le topic {msg.topic}")
    try:
        base_data = json.loads(msg.payload.decode("utf-8"))
        print("Données de base :", base_data)

        simulated_data = simulate_multiple_sensors(base_data)

        for data in simulated_data:
            if data["message_id"] in seen_ids:
                print("🔁 Doublon détecté, ignoré.")
                continue

            seen_ids.add(data["message_id"])
            save_data(data)
            print(f"✅ Données sauvegardées pour capteur {data['id_capteur']}")

    except Exception as e:
        print("❌ Erreur de parsing JSON :", e)


# MQTT
client = mqtt.Client()
client.on_message = on_message

client.connect("51.38.185.58", 1883, 60)
client.subscribe("capteurs/kn/data")

print("🕵️ En attente de messages simulés...")
client.loop_forever()
import paho.mqtt.client as mqtt
import json
import threading
import uuid
from copy import deepcopy

seen_ids = set()
DATA_FILE = "capteurs_data.json"
lock = threading.Lock()

def save_data(data, filename=DATA_FILE):
    lock.acquire()
    try:
        try:
            with open(filename, "r") as f:
                existing = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing = []

        found = False
        for i, d in enumerate(existing):
            if d.get("message_id") == data.get("message_id"):
                existing[i] = data
                found = True
                break
        if not found:
            existing.append(data)

        with open(filename, "w") as f:
            json.dump(existing, f, indent=2)
    finally:
        lock.release()


# Fonction pour simuler plusieurs capteurs à partir d’un seul message
def simulate_multiple_sensors(base_data):
    simulated = []

    capteurs = [
        {"id": "temp_1", "pos": "serre_nord"},
        {"id": "temp_2", "pos": "serre_sud"},
        {"id": "humid_1", "pos": "serre_est"},
        {"id": "humid_2", "pos": "serre_ouest"}
    ]

    for cap in capteurs:
        data = deepcopy(base_data)
        data["id_capteur"] = cap["id"]
        data["position"] = cap["pos"]
        data["message_id"] = str(uuid.uuid4())  # message unique
        simulated.append(data)

    return simulated


def on_message(client, userdata, msg):
    print(f"\n📩 Message reçu sur le topic {msg.topic}")
    try:
        base_data = json.loads(msg.payload.decode("utf-8"))
        print("Données de base :", base_data)

        simulated_data = simulate_multiple_sensors(base_data)

        for data in simulated_data:
            if data["message_id"] in seen_ids:
                print("🔁 Doublon détecté, ignoré.")
                continue

            seen_ids.add(data["message_id"])
            save_data(data)
            print(f"✅ Données sauvegardées pour capteur {data['id_capteur']}")

    except Exception as e:
        print("❌ Erreur de parsing JSON :", e)


# MQTT
client = mqtt.Client()
client.on_message = on_message

client.connect("51.38.185.58", 1883, 60)
client.subscribe("capteurs/kn/data")

print("🕵️ En attente de messages simulés...")
client.loop_forever()