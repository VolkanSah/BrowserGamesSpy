import psutil
from selenium import webdriver
import time
import tkinter as tk
from tkinter import ttk
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def get_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    net_io = psutil.net_io_counters()
    sent_bytes = net_io.bytes_sent
    recv_bytes = net_io.bytes_recv
    
    return cpu_usage, memory_usage, sent_bytes, recv_bytes

def get_network_connections():
    connections = psutil.net_connections(kind='inet')
    active_connections = []
    for conn in connections:
        if conn.status == psutil.CONN_ESTABLISHED:
            active_connections.append((conn.laddr.ip, conn.laddr.port, conn.raddr.ip, conn.raddr.port))
    return active_connections

def update_metrics():
    cpu_usage, memory_usage, sent_bytes, recv_bytes = get_system_metrics()
    active_connections = get_network_connections()

    cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
    memory_label.config(text=f"Memory Usage: {memory_usage}%")
    sent_label.config(text=f"Network Sent: {sent_bytes} bytes")
    recv_label.config(text=f"Network Received: {recv_bytes} bytes")
    
    connections_text.delete(1.0, tk.END)
    connections_text.insert(tk.END, "Active Network Connections:\n")
    for conn in active_connections:
        connections_text.insert(tk.END, f"Local: {conn[0]}:{conn[1]} -> Remote: {conn[2]}:{conn[3]}\n")
    
    data.append([cpu_usage, memory_usage, sent_bytes, recv_bytes, active_connections])
    
    plot_data()
    
    root.after(5000, update_metrics)

def save_data():
    with open('system_metrics.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["CPU Usage", "Memory Usage", "Network Sent", "Network Received", "Connections"])
        for row in data:
            writer.writerow(row[:4] + [str(row[4])])

def plot_data():
    if len(data) > 1:
        cpu_data = [row[0] for row in data]
        memory_data = [row[1] for row in data]
        sent_data = [row[2] for row in data]
        recv_data = [row[3] for row in data]

        time_points = list(range(len(data)))

        fig.clear()

        ax1 = fig.add_subplot(221)
        ax1.plot(time_points, cpu_data, label='CPU Usage')
        ax1.set_title('CPU Usage (%)')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Usage (%)')

        ax2 = fig.add_subplot(222)
        ax2.plot(time_points, memory_data, label='Memory Usage')
        ax2.set_title('Memory Usage (%)')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Usage (%)')

        ax3 = fig.add_subplot(223)
        ax3.plot(time_points, sent_data, label='Network Sent')
        ax3.set_title('Network Sent (bytes)')
        ax3.set_xlabel('Time')
        ax3.set_ylabel('Bytes')

        ax4 = fig.add_subplot(224)
        ax4.plot(time_points, recv_data, label='Network Received')
        ax4.set_title('Network Received (bytes)')
        ax4.set_xlabel('Time')
        ax4.set_ylabel('Bytes')

        canvas.draw()

def main():
    global root, cpu_label, memory_label, sent_label, recv_label, connections_text, data, fig, canvas
    
    url = "https://www.diesiedleronline.de/"
    
    # Start the browser
    driver = webdriver.Chrome()
    driver.get(url)
    
    data = []
    
    # Set up the GUI
    root = tk.Tk()
    root.title("System and Network Monitoring")

    cpu_label = ttk.Label(root, text="CPU Usage: ")
    cpu_label.pack()
    
    memory_label = ttk.Label(root, text="Memory Usage: ")
    memory_label.pack()
    
    sent_label = ttk.Label(root, text="Network Sent: ")
    sent_label.pack()
    
    recv_label = ttk.Label(root, text="Network Received: ")
    recv_label.pack()
    
    connections_text = tk.Text(root, height=10, width=50)
    connections_text.pack()
    
    save_button = ttk.Button(root, text="Save Data", command=save_data)
    save_button.pack()
    
    fig = plt.Figure(figsize=(10, 8), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    # Update the metrics every 5 seconds
    root.after(5000, update_metrics)
    
    # Run the GUI
    root.mainloop()
    
    # Close the browser when the GUI is closed
    driver.quit()

if __name__ == "__main__":
    main()
