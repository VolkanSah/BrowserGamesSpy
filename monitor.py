import psutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import tkinter as tk
from tkinter import ttk, messagebox
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import logging
import json
import os
import threading

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
        logging.info(f"New connection detected: {json.dumps(connection_info, ensure_ascii=False)}")
    
    def get_ip_location(self, ip):
        # Placeholder for potential geolocation service
        if ip.startswith(('192.168.', '10.', '172.')):
            return 'Local Network'
        return 'External IP'

def setup_logging():
    """Configure logging for the application"""
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    
    current_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = os.path.join(log_dir, f'monitoring_{current_time}.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def get_system_metrics():
    """Collect and log system performance metrics"""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    net_io = psutil.net_io_counters()
    sent_bytes = net_io.bytes_sent
    recv_bytes = net_io.bytes_recv
    
    logging.info(f"System Metrics - CPU: {cpu_usage}%, RAM: {memory_usage}%, "
                f"Network Sent: {sent_bytes}, Received: {recv_bytes}")
    
    return cpu_usage, memory_usage, sent_bytes, recv_bytes

def get_network_connections(network_monitor):
    """Track and log network connections"""
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
            
            if connection_tuple not in network_monitor.previous_connections:
                network_monitor.log_connection_change(connection_tuple)
    
    network_monitor.previous_connections = current_connections
    return active_connections

def collect_browser_console_logs(driver, log_all_console):
    """
    Collect and log browser console messages
    
    Args:
        driver (WebDriver): Active Selenium WebDriver instance
        log_all_console (bool): Flag to collect all logs or only errors
    """
    try:
        browser_logs = driver.get_log('browser')
        
        # Filter logs based on user preference
        if not log_all_console:
            browser_logs = [
                log for log in browser_logs 
                if log['level'] in ['SEVERE', 'ERROR']
            ]
        
        if browser_logs:
            logging.info(f"Browser Console Logs found: {len(browser_logs)} entries")
            
            # Create logs directory if not exists
            console_log_dir = 'browser_console_logs'
            os.makedirs(console_log_dir, exist_ok=True)
            
            # Generate filename with timestamp
            current_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            log_filename = os.path.join(console_log_dir, f'browser_console_{current_time}.log')
            
            # Write logs to file
            with open(log_filename, 'w', encoding='utf-8') as log_file:
                for log_entry in browser_logs:
                    log_entry_str = (
                        f"Timestamp: {log_entry['timestamp']} | "
                        f"Level: {log_entry['level']} | "
                        f"Message: {log_entry['message']}\n"
                    )
                    log_file.write(log_entry_str)
                    logging.warning(log_entry_str)
            
            logging.info(f"Browser Console Logs saved to {log_filename}")
    
    except Exception as e:
        logging.error(f"Error collecting browser console logs: {str(e)}")

def save_system_metrics(data):
    """Save system metrics to CSV"""
    current_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'system_metrics_{current_time}.csv'
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Timestamp", "CPU Usage", "Memory Usage", 
            "Network Sent", "Network Received", "Connections"
        ])
        for row in data:
            writer.writerow(row)
    
    logging.info(f"Data saved to {filename}")
    return filename

class MonitoringApp:
    def __init__(self, url):
        self.url = url
        self.network_monitor = NetworkMonitor()
        self.data = []
        self.log_all_console = False
        
        # Setup logging
        setup_logging()
        
        # Initialize main window
        self.root = tk.Tk()
        self.root.title("System and Network Monitoring Tool")
        
        # Setup WebDriver
        self.setup_webdriver()
        
        # Create GUI
        self.create_gui()
        
    def setup_webdriver(self):
        """Configure and start WebDriver"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--enable-logging')
            chrome_options.add_argument('--v=1')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.get(self.url)
            logging.info(f"Browser started successfully for URL: {self.url}")
        except Exception as e:
            logging.error(f"Error starting browser: {str(e)}")
            messagebox.showerror("Browser Error", str(e))
            self.root.quit()
    
    def create_gui(self):
        """Create the main application GUI"""
        # Metrics Labels
        self.cpu_label = ttk.Label(self.root, text="CPU Usage: 0%")
        self.cpu_label.pack(pady=5)
        
        self.memory_label = ttk.Label(self.root, text="Memory Usage: 0%")
        self.memory_label.pack(pady=5)
        
        self.sent_label = ttk.Label(self.root, text="Network Sent: 0 Bytes")
        self.sent_label.pack(pady=5)
        
        self.recv_label = ttk.Label(self.root, text="Network Received: 0 Bytes")
        self.recv_label.pack(pady=5)
        
        # Connections Text Area
        self.connections_text = tk.Text(self.root, height=10, width=50)
        self.connections_text.pack(pady=10)
        
        # Console Log Checkbox
        self.log_all_console_var = tk.BooleanVar(value=False)
        self.log_console_checkbox = ttk.Checkbutton(
            self.root, 
            text="Save All Console Logs (not just errors)", 
            variable=self.log_all_console_var
        )
        self.log_console_checkbox.pack(pady=5)
        
        # Plotting Checkboxes
        self.show_cpu = tk.BooleanVar(value=True)
        self.show_memory = tk.BooleanVar(value=True)
        self.show_sent = tk.BooleanVar(value=True)
        self.show_recv = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(self.root, text="Show CPU", variable=self.show_cpu, command=self.plot_data).pack()
        ttk.Checkbutton(self.root, text="Show Memory", variable=self.show_memory, command=self.plot_data).pack()
        ttk.Checkbutton(self.root, text="Show Network Sent", variable=self.show_sent, command=self.plot_data).pack()
        ttk.Checkbutton(self.root, text="Show Network Received", variable=self.show_recv, command=self.plot_data).pack()
        
        # Matplotlib Figure
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()
        
        # Save Data Button
        save_button = ttk.Button(self.root, text="Save Metrics", command=self.save_metrics)
        save_button.pack(pady=10)
        
        # Start metrics update
        self.update_metrics()
    
    def update_metrics(self):
        """Update system and network metrics"""
        try:
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logging.info(f"Updating metrics: {current_time}")
            
            # Collect console logs
            collect_browser_console_logs(self.driver, self.log_all_console_var.get())
            
            # Get system metrics
            cpu_usage, memory_usage, sent_bytes, recv_bytes = get_system_metrics()
            active_connections = get_network_connections(self.network_monitor)
            
            # Update labels
            self.cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
            self.memory_label.config(text=f"Memory Usage: {memory_usage}%")
            self.sent_label.config(text=f"Network Sent: {sent_bytes} Bytes")
            self.recv_label.config(text=f"Network Received: {recv_bytes} Bytes")
            
            # Update connections text
            self.connections_text.delete(1.0, tk.END)
            self.connections_text.insert(tk.END, f"Active Network Connections ({current_time}):\n")
            for conn in active_connections:
                connection_str = f"Local: {conn[0]}:{conn[1]} -> Remote: {conn[2]}:{conn[3]}\n"
                self.connections_text.insert(tk.END, connection_str)
            
            # Store data for plotting and saving
            self.data.append([current_time, cpu_usage, memory_usage, sent_bytes, recv_bytes, active_connections])
            
            # Plot data
            self.plot_data()
            
            # Schedule next update
            self.root.after(5000, self.update_metrics)
        
        except Exception as e:
            logging.error(f"Error updating metrics: {str(e)}")
    
    def plot_data(self):
        """Plot system metrics"""
        if len(self.data) > 1:
            self.fig.clear()
            
            timestamps = [row[0] for row in self.data]
            cpu_data = [row[1] for row in self.data]
            memory_data = [row[2] for row in self.data]
            sent_data = [row[3] for row in self.data]
            recv_data = [row[4] for row in self.data]
            
            # Plot based on checkbox selections
            plots_to_create = []
            if self.show_cpu.get(): plots_to_create.append(('CPU Usage (%)', cpu_data, 221))
            if self.show_memory.get(): plots_to_create.append(('Memory Usage (%)', memory_data, 222))
            if self.show_sent.get(): plots_to_create.append(('Network Sent (Bytes)', sent_data, 223))
            if self.show_recv.get(): plots_to_create.append(('Network Received (Bytes)', recv_data, 224))
            
            for title, data, subplot_pos in plots_to_create:
                ax = self.fig.add_subplot(subplot_pos)
                ax.plot(range(len(timestamps)), data)
                ax.set_title(title)
                ax.set_xlabel('Time')
                ax.set_ylabel(title.split()[0])
            
            self.canvas.draw()
    
    def save_metrics(self):
        """Save system metrics to CSV"""
        filename = save_system_metrics(self.data)
        messagebox.showinfo("Metrics Saved", f"Metrics saved to {filename}")
    
    def run(self):
        """Start the application main loop"""
        try:
            logging.info("Monitoring Tool Started")
            self.root.mainloop()
        except Exception as e:
            logging.error(f"Application Error: {str(e)}")
        finally:
            logging.info("Monitoring Tool Closing")
            self.driver.quit()

def main():
    monitoring_app = MonitoringApp("https://www.diesiedleronline.de/")
    monitoring_app.run()

if __name__ == "__main__":
    main()
