import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from kafka import KafkaConsumer
import json
import threading
import os

class KafkaDataGrapher:
    def __init__(self, master):
        self.master = master
        self.master.title("Kafka Data Grapher")

        # Setup the plot
        self.figure = Figure(figsize=(6, 5), dpi=100)
        self.plot = self.figure.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasTkAgg(self.figure, master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Kafka setup (customize your Kafka settings here)
        self.consumer = KafkaConsumer(
            'stock_data',
            bootstrap_servers=[f'{os.env}:9092'],
            auto_offset_reset='earliest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        # Start the thread to poll Kafka and update the plot
        self.polling = True
        self.thread = threading.Thread(target=self.poll_kafka)
        self.thread.start()

        # Stop polling when the GUI is closed
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def poll_kafka(self):
        """Polls Kafka for data and updates the plot."""
        x_data = []
        y_data = []
        for message in self.consumer:
            if not self.polling:
                break
            data = message.value
            x_data.append(data['timestamp'])  # Assume there's a timestamp field
            y_data.append(data['value'])  # Assume there's a value field

            # Update plot
            self.plot.clear()
            self.plot.plot(x_data, y_data)
            self.canvas.draw()

            if len(x_data) > 50:  # Keep the last 50 points
                x_data.pop(0)
                y_data.pop(0)

    def on_closing(self):
        """Handles the GUI closing event."""
        self.polling = False
        self.thread.join()
        self.consumer.close()
        self.master.destroy()

def main():
    root = tk.Tk()
    app = KafkaDataGrapher(root)
    root.mainloop()

if __name__ == "__main__":
    main()
