# data_generator.py

import random
import json
from datetime import datetime

class DataGenerator:
    @staticmethod
    def generate_data():
        """ Simulated temperature data with slight fluctuation """
        base = 25  # Base temperature
        fluctuation = random.uniform(-5, 5)
        return round(base + fluctuation, 2)
    
    @staticmethod
    def package_data(value):
        packet = {
            "packet_id": random.randint(1000, 9999),
            "timestamp": datetime.now().isoformat(),
            "value": value
        }
        return json.dumps(packet)
