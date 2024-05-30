import psutil
from selenium import webdriver
import time

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

def print_metrics(cpu, memory, sent, recv):
    print(f"CPU Usage: {cpu}%")
    print(f"Memory Usage: {memory}%")
    print(f"Network Sent: {sent} bytes")
    print(f"Network Received: {recv} bytes")

def print_connections(connections):
    print("Active Network Connections:")
    for conn in connections:
        print(f"Local: {conn[0]}:{conn[1]} -> Remote: {conn[2]}:{conn[3]}")

def main():
    url = "https://url_of_browsergame.tld/"
    
    # Start the browser
    driver = webdriver.Chrome()
    driver.get(url)
    
    try:
        while True:
            cpu_usage, memory_usage, sent_bytes, recv_bytes = get_system_metrics()
            active_connections = get_network_connections()
            print_metrics(cpu_usage, memory_usage, sent_bytes, recv_bytes)
            print_connections(active_connections)
            time.sleep(5)  # Check every 5 seconds
    except KeyboardInterrupt:
        print("Stopping the monitoring...")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
