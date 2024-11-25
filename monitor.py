import psutil
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import tkinter as tk
from tkinter import ttk
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import logging
import json
import os

# Logging-Konfiguration
def setup_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    current_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = f'logs/monitoring_{current_time}.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )

class NetworkMonitor:
    def __init__(self):
        self.session_start = datetime.datetime.now()
        self.previous_connections = set()
        self.connection_history = []
    
    def log_connection_change(self, new_connection):
        timestamp = datetime.datetime.now()
        connection_info = {
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'local_ip': new_connection[0],
            'local_port': new_connection[1],
            'remote_ip': new_connection[2],
            'remote_port': new_connection[3],
            'location': self.get_ip_location(new_connection[2])
        }
        self.connection_history.append(connection_info)
        logging.info(f"Neue Verbindung erkannt: {json.dumps(connection_info, ensure_ascii=False)}")
    
    def get_ip_location(self, ip):
        # Hier könnte man einen Geolocation-Service einbinden
        # Beispiel-Implementierung:
        if ip.startswith('192.168.') or ip.startswith('10.') or ip.startswith('172.'):
            return 'Lokales Netzwerk'
        return 'Externe IP'

def get_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    net_io = psutil.net_io_counters()
    sent_bytes = net_io.bytes_sent
    recv_bytes = net_io.bytes_recv
    
    # Logging der Systemmetriken
    logging.info(f"System Metriken - CPU: {cpu_usage}%, RAM: {memory_usage}%, "
                f"Netzwerk Gesendet: {sent_bytes}, Empfangen: {recv_bytes}")
    
    return cpu_usage, memory_usage, sent_bytes, recv_bytes

def get_network_connections(network_monitor):
    connections = psutil.net_connections(kind='inet')
    active_connections = []
    current_connections = set()
    
    for conn in connections:
        if conn.status == psutil.CONN_ESTABLISHED:
            connection_tuple = (conn.laddr.ip, conn.laddr.port, 
                              conn.raddr.ip if conn.raddr else 'None', 
                              conn.raddr.port if conn.raddr else 0)
            active_connections.append(connection_tuple)
            current_connections.add(connection_tuple)
            
            # Überprüfen auf neue Verbindungen
            if connection_tuple not in network_monitor.previous_connections:
                network_monitor.log_connection_change(connection_tuple)
    
    network_monitor.previous_connections = current_connections
    return active_connections

def update_metrics(network_monitor):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"Update der Metriken gestartet: {current_time}")
    
    cpu_usage, memory_usage, sent_bytes, recv_bytes = get_system_metrics()
    active_connections = get_network_connections(network_monitor)

    cpu_label.config(text=f"CPU Auslastung: {cpu_usage}%")
    memory_label.config(text=f"Speicherauslastung: {memory_usage}%")
    sent_label.config(text=f"Netzwerk Gesendet: {sent_bytes} Bytes")
    recv_label.config(text=f"Netzwerk Empfangen: {recv_bytes} Bytes")
    
    connections_text.delete(1.0, tk.END)
    connections_text.insert(tk.END, f"Aktive Netzwerkverbindungen ({current_time}):\n")
    for conn in active_connections:
        connection_str = f"Lokal: {conn[0]}:{conn[1]} -> Remote: {conn[2]}:{conn[3]}\n"
        connections_text.insert(tk.END, connection_str)
    
    data.append([current_time, cpu_usage, memory_usage, sent_bytes, recv_bytes, active_connections])
    
    plot_data()
    
    root.after(5000, lambda: update_metrics(network_monitor))

def save_data():
    current_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'system_metrics_{current_time}.csv'
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Zeitstempel", "CPU Auslastung", "Speicherauslastung", 
                        "Netzwerk Gesendet", "Netzwerk Empfangen", "Verbindungen"])
        for row in data:
            writer.writerow(row)
    
    logging.info(f"Daten wurden in {filename} gespeichert")

def plot_data():
    if len(data) > 1:
        timestamps = [row[0] for row in data]
        cpu_data = [row[1] for row in data]
        memory_data = [row[2] for row in data]
        sent_data = [row[3] for row in data]
        recv_data = [row[4] for row in data]

        fig.clear()

        if show_cpu.get():
            ax1 = fig.add_subplot(221)
            ax1.plot(range(len(timestamps)), cpu_data, label='CPU')
            ax1.set_title('CPU Auslastung (%)')
            ax1.set_xlabel('Zeit')
            ax1.set_ylabel('Auslastung (%)')

        if show_memory.get():
            ax2 = fig.add_subplot(222)
            ax2.plot(range(len(timestamps)), memory_data, label='RAM')
            ax2.set_title('Speicherauslastung (%)')
            ax2.set_xlabel('Zeit')
            ax2.set_ylabel('Auslastung (%)')

        if show_sent.get():
            ax3 = fig.add_subplot(223)
            ax3.plot(range(len(timestamps)), sent_data, label='Gesendet')
            ax3.set_title('Netzwerk Gesendet (Bytes)')
            ax3.set_xlabel('Zeit')
            ax3.set_ylabel('Bytes')

        if show_recv.get():
            ax4 = fig.add_subplot(224)
            ax4.plot(range(len(timestamps)), recv_data, label='Empfangen')
            ax4.set_title('Netzwerk Empfangen (Bytes)')
            ax4.set_xlabel('Zeit')
            ax4.set_ylabel('Bytes')

        canvas.draw()

def main():
    global root, cpu_label, memory_label, sent_label, recv_label, connections_text, data, fig, canvas
    global show_cpu, show_memory, show_sent, show_recv
    
    setup_logging()
    network_monitor = NetworkMonitor()
    
    logging.info("Monitoring-Tool gestartet")
    url = "https://www.diesiedleronline.de/"
    
    try:
        logging.info(f"Starte Browser für URL: {url}")
        driver = webdriver.Chrome()
        driver.get(url)
        logging.info("Browser erfolgreich gestartet")
    except Exception as e:
        logging.error(f"Fehler beim Starten des Browsers: {str(e)}")
        return
    
    data = []
    
    root = tk.Tk()
    root.title("System- und Netzwerk-Monitoring für Die Siedler Online")

    # GUI-Elemente erstellen...
    [Rest des GUI-Codes bleibt unverändert]

    # Update der Metriken alle 5 Sekunden
    root.after(5000, lambda: update_metrics(network_monitor))
    
    root.mainloop()
    
    logging.info("Monitoring-Tool wird beendet")
    driver.quit()

if __name__ == "__main__":
    main()
