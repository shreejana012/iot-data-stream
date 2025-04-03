# main.py
import tkinter as tk
from group_10_publisher import PublisherGUI, Publisher
from group_10_subscriber import SubscriberGUI, Subscriber

if __name__ == "__main__":
    root = tk.Tk()
    root.title("MQTT IoT System")

    # Publisher
    publisher = Publisher()
    pub_gui = PublisherGUI(root, publisher)

    # Subscriber
    subscriber = Subscriber()
    sub_gui = SubscriberGUI(root, subscriber)

    root.mainloop()