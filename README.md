# BrowserGamesSpy 
###### System and Network Monitoring Tool

This tool monitors system metrics and network connections for browser-based games like "Die Siedler Online". It collects data on CPU usage, memory usage, network activity, and active network connections, and displays these metrics in a graphical user interface (GUI) using `tkinter`. Additionally, the tool can save the collected data to a CSV file and visualize the metrics using `matplotlib`.

## Features
- Monitors CPU usage, memory usage, network sent/received bytes, and active network connections.
- Displays metrics in a `tkinter` GUI with real-time updates.
- Allows the user to select which metrics to display using checkboxes.
- Saves collected data to a CSV file.
- Visualizes metrics in plots using `matplotlib`.

## Requirements
- Python 3.x
- `psutil` library for system metrics
- `selenium` library for browser interaction
- `tkinter` library for the GUI
- `csv` module for saving data
- `matplotlib` library for plotting data
- ChromeDriver for `selenium` (ensure it is in the PATH)

## Installation
1. Install the required libraries:
    ```bash
    pip install psutil selenium matplotlib
    ```

2. Download and install [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) and ensure it is in your PATH.

## Usage
1. Clone the repository or download the script.
2. Run the script:
    ```bash
    python monitor.py
    ```

3. The GUI will open and start monitoring the specified URL (https://www.diesiedleronline.de/).

4. Use the checkboxes to select which metrics to display in the plots.

5. Click the "Save Data" button to save the collected data to a CSV file.

## Code Explanation
The code consists of the following main parts:

1. **Imports and Functions**:
    - Import necessary libraries.
    - Define functions to get system metrics and network connections.

2. **Update Metrics**:
    - Collect metrics every 5 seconds.
    - Update the GUI with the latest metrics.
    - Append collected data to a list for future reference or saving.

3. **Save Data**:
    - Save the collected data to a CSV file when the "Save Data" button is clicked.

4. **Plot Data**:
    - Plot the selected metrics in the GUI using `matplotlib`.

5. **Main Function**:
    - Set up the `tkinter` GUI.
    - Start the Chrome browser using `selenium`.
    - Begin the monitoring and updating loop.

## Example Code
Here is the complete script:

```python
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
    connections_text.insert(tk.END, "Active Network Connections:
")
    for conn in active_connections:
        connections_text.insert(tk.END, f"Local: {conn[0]}:{conn[1]} -> Remote: {conn[2]}:{conn[3]}
")
    
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

        if show_cpu.get():
            ax1 = fig.add_subplot(221)
            ax1.plot(time_points, cpu_data, label='CPU Usage')
            ax1.set_title('CPU Usage (%)')
            ax1.set_xlabel('Time')
            ax1.set_ylabel('Usage (%)')

        if show_memory.get():
            ax2 = fig.add_subplot(222)
            ax2.plot(time_points, memory_data, label='Memory Usage')
            ax2.set_title('Memory Usage (%)')
            ax2.set_xlabel('Time')
            ax2.set_ylabel('Usage (%)')

        if show_sent.get():
            ax3 = fig.add_subplot(223)
            ax3.plot(time_points, sent_data, label='Network Sent')
            ax3.set_title('Network Sent (bytes)')
            ax3.set_xlabel('Time')
            ax3.set_ylabel('Bytes')

        if show_recv.get():
            ax4 = fig.add_subplot(224)
            ax4.plot(time_points, recv_data, label='Network Received')
            ax4.set_title('Network Received (bytes)')
            ax4.set_xlabel('Time')
            ax4.set_ylabel('Bytes')

        canvas.draw()

def main():
    global root, cpu_label, memory_label, sent_label, recv_label, connections_text, data, fig, canvas
    global show_cpu, show_memory, show_sent, show_recv
    
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

    # Checkbox options for metrics
    show_cpu = tk.BooleanVar(value=True)
    show_memory = tk.BooleanVar(value=True)
    show_sent = tk.BooleanVar(value=True)
    show_recv = tk.BooleanVar(value=True)

    ttk.Checkbutton(root, text="Show CPU Usage", variable=show_cpu, command=plot_data).pack()
    ttk.Checkbutton(root, text="Show Memory Usage", variable=show_memory, command=plot_data).pack()
    ttk.Checkbutton(root, text="Show Network Sent", variable=show_sent, command=plot_data).pack()
    ttk.Checkbutton(root, text="Show Network Received", variable=show_recv, command=plot_data).pack()

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
```

## License
This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details.
