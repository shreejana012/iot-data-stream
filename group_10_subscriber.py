# subscriber.py

import paho.mqtt.client as mqtt
import json
import tkinter as tk

BROKER = "localhost"
PORT = 1883
TOPIC = "iot/data"

class Subscriber:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(BROKER, PORT, 60)
        self.client.loop_start()

        self.gui = None

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to broker")
        self.client.subscribe(TOPIC)

    def on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
            message = f"Received: {data}"
            
            # Handle missing or corrupted data
            if isinstance(data, str) and "CORRUPTED" in data:
                message = "Received Corrupted Data!"
            elif "value" in data:
                value = data["value"]
                if value < 10 or value > 40:  # Example range check
                    message += "Out of range!"
            else:
                message = "Missing or Invalid Data!"

            print(message)
            if self.gui:
                self.gui.display_message(message)
        except json.JSONDecodeError:
            print("Received corrupted data!")

class SubscriberGUI:
    def __init__(self, root, subscriber):
        self.root = root
        self.subscriber = subscriber
        self.subscriber.gui = self

        self.label = tk.Label(root, text="MQTT Subscriber", font=("Arial", 14))
        self.label.pack()

        self.text_box = tk.Text(root, height=10, width=50)
        self.text_box.pack()

    def display_message(self, message):
        self.text_box.insert(tk.END, message + "\n")
        self.text_box.see(tk.END)
