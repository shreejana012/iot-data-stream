# publisher.py

import paho.mqtt.client as mqtt
import time
import random
import tkinter as tk
from threading import Thread
from group_10_data_generator import DataGenerator

BROKER = "localhost"
PORT = 1883
TOPIC = "iot/data"

class Publisher:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect(BROKER, PORT, 60)
        self.running = False
        self.interval = 2  # Default interval in seconds
        self.corruption_chance = 1  # 1% corruption probability

    def publish_data(self):
        while self.running:
            value = DataGenerator.generate_data()
            packet = DataGenerator.package_data(value)

            # Simulating random transmission skips
            if random.randint(1, 100) <= 5:  # 5% chance to skip a block
                print("Skipping transmission...")
                time.sleep(self.interval * 3)
                continue
            
            # Corrupting data
            if random.randint(1, 100) <= self.corruption_chance:
                packet = "!!!CORRUPTED DATA!!!"

            self.client.publish(TOPIC, packet)
            print(f"Published: {packet}")
            time.sleep(self.interval)

    def start_publishing(self):
        if not self.running:
            self.running = True
            Thread(target=self.publish_data, daemon=True).start()

    def stop_publishing(self):
        self.running = False

class PublisherGUI:
    def __init__(self, root, publisher):
        self.root = root
        self.publisher = publisher
        
        self.label = tk.Label(root, text="MQTT Publisher", font=("Arial", 14))
        self.label.pack()

        self.interval_label = tk.Label(root, text="Interval (seconds):")
        self.interval_label.pack()
        self.interval_entry = tk.Entry(root)
        self.interval_entry.pack()
        self.interval_entry.insert(0, "2")

        self.corrupt_label = tk.Label(root, text="Corruption %:")
        self.corrupt_label.pack()
        self.corrupt_entry = tk.Entry(root)
        self.corrupt_entry.pack()
        self.corrupt_entry.insert(0, "1")

        self.start_btn = tk.Button(root, text="Start Publishing", command=self.start_publishing)
        self.start_btn.pack()
        
        self.stop_btn = tk.Button(root, text="Stop Publishing", command=self.publisher.stop_publishing)
        self.stop_btn.pack()

    def start_publishing(self):
        self.publisher.interval = int(self.interval_entry.get())
        self.publisher.corruption_chance = int(self.corrupt_entry.get())
        self.publisher.start_publishing()
