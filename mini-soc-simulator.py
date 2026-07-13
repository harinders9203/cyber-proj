import socket
import time
import os
import subprocess
from collections import Counter

# GLOBAL DATA
alerts = []
open_ports = []
packet_count = Counter()
SAMPLE_ALERT_LOG = """[**] [1:1000001:1] TCP Port Scan Detected [**]
07/13-09:40:10.100000 192.168.1.25:49612 -> 192.168.1.10:22
[**] [1:1000002:1] SQL Injection Attempt [**]
07/13-09:41:42.220000 10.10.15.8:44321 -> 192.168.1.10:80
[**] [1:1000003:1] SSH Brute Force Attempt [**]
07/13-09:43:15.887000 172.16.1.50:51844 -> 192.168.1.10:22
[**] [1:1000004:1] Suspicious SSH Activity [**]
07/13-09:44:01.501000 203.0.113.45:60222 -> 192.168.1.10:22
"""

# PORT SCANNER

def scan_ports(host, start_port, end_port):

    print("\nScanning Ports...\n")

    ip = socket.gethostbyname(host)

    for port in range(start_port, end_port + 1):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)

        result = s.connect_ex((ip, port))

        if result == 0:

            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"

            print(f"[OPEN] {port} ({service})")

            open_ports.append((port, service))

        s.close()

# NETWORK MONITOR

def get_connection_snapshot():

    try:
        result = subprocess.run(
            ["netstat", "-ano"],
            capture_output=True,
            text=True,
            check=False
        )
    except FileNotFoundError:
        return set()

    connections = set()

    for line in result.stdout.splitlines():
        parts = line.split()

        if not parts:
            continue

        protocol = parts[0].upper()

        if protocol == "TCP" and len(parts) >= 5:
            connections.add((parts[0], parts[1], parts[2], parts[3], parts[4]))

        elif protocol == "UDP" and len(parts) >= 4:
            connections.add((parts[0], parts[1], parts[2], "STATELESS", parts[3]))

    return connections


def monitor_with_connection_sampling(seconds):

    print("Raw socket capture unavailable. Falling back to connection sampling...\n")

    previous_snapshot = set()
    peak_connections = 0
    samples = 0
    start = time.time()

    while time.time() - start < seconds:

        current_snapshot = get_connection_snapshot()
        active_connections = len(current_snapshot)
        new_connections = len(current_snapshot - previous_snapshot)

        packet_count["Packets"] += active_connections + new_connections
        packet_count["Connection Samples"] += 1
        peak_connections = max(peak_connections, active_connections)
        samples += 1

        print(
            f"Sample {samples}: "
            f"active connections={active_connections}, "
            f"new activity={new_connections}"
        )

        previous_snapshot = current_snapshot
        time.sleep(1)

    packet_count["Peak Active Connections"] = max(
        packet_count["Peak Active Connections"],
        peak_connections
    )


def monitor_with_raw_socket(seconds):

    s = socket.socket(
        socket.AF_INET,
        socket.SOCK_RAW,
        socket.IPPROTO_IP
    )

    host = socket.gethostbyname(socket.gethostname())

    s.bind((host, 0))
    s.settimeout(1.0)
    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    start = time.time()

    try:
        while time.time() - start < seconds:
            try:
                s.recvfrom(65565)
                packet_count["Packets"] += 1
            except socket.timeout:
                continue
    finally:
        s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        s.close()


def monitor_network(seconds=5):

    print("\nMonitoring Network...")

    try:
        monitor_with_raw_socket(seconds)
        print(f"Monitoring complete. Packets captured: {packet_count['Packets']}")

    except Exception:
        monitor_with_connection_sampling(seconds)
        print(
            "Monitoring complete. "
            f"Observed activity score: {packet_count['Packets']}"
        )

# SNORT LOG ANALYZER

def create_sample_log(file_name="alerts.log"):

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(SAMPLE_ALERT_LOG)


def analyze_logs(file_name="alerts.log"):

    print("\nReading Snort Logs...\n")

    if not os.path.exists(file_name):

        create_sample_log(file_name)
        print(f"Created sample log file: {file_name}")

    alerts.clear()

    with open(file_name, "r", encoding="utf-8", errors="ignore") as f:

        for line in f:
            line_upper = line.upper().strip()

            if not line_upper or "->" in line_upper:
                continue

            if "SCAN" in line_upper:
                alerts.append(("Medium", "Port Scan"))

            elif "SQL" in line_upper:
                alerts.append(("High", "SQL Injection Attempt"))

            elif "BRUTE" in line_upper:
                alerts.append(("High", "Brute Force"))

            elif "SSH" in line_upper:
                alerts.append(("Medium", "SSH Activity"))

            elif "[**]" in line_upper:
                alerts.append(("Low", "Unknown Event"))

    print("Alerts Loaded:", len(alerts))


# INCIDENT DASHBOARD

def dashboard():

    print("\n")
    print("=" * 55)
    print("        MINI SECURITY OPERATIONS CENTER")
    print("=" * 55)

    print("\nOpen Ports:", len(open_ports))

    for port, service in open_ports:
        print(f"  {port} ({service})")

    print("\nAlerts:", len(alerts))

    risk = Counter()

    for level, attack in alerts:
        risk[level] += 1

    print("\nRisk Summary")

    print("Critical :", risk["Critical"])
    print("High     :", risk["High"])
    print("Medium   :", risk["Medium"])
    print("Low      :", risk["Low"])

    print("\nPackets Captured:", packet_count["Packets"])
    print("Connection Samples:", packet_count["Connection Samples"])
    print("Peak Active Connections:", packet_count["Peak Active Connections"])

    print("=" * 55)


# REPORT

def generate_report():

    with open("Security_Report.txt", "w") as f:

        f.write("MINI SOC REPORT\n")
        f.write("=" * 50 + "\n\n")

        f.write("Open Ports\n")

        for port, service in open_ports:
            f.write(f"{port} ({service})\n")

        f.write("\nDetected Alerts\n")

        for level, attack in alerts:
            f.write(f"{level} : {attack}\n")

        f.write("\nPackets Captured\n")
        f.write(str(packet_count["Packets"]))
        f.write("\n\nConnection Samples\n")
        f.write(str(packet_count["Connection Samples"]))
        f.write("\n\nPeak Active Connections\n")
        f.write(str(packet_count["Peak Active Connections"]))

    print("\nReport Generated: Security_Report.txt")


# MENU

def menu():

    while True:

        print("\n")
        print("=" * 40)
        print(" MINI SOC ")
        print("=" * 40)

        print("1. Scan Ports")
        print("2. Monitor Network")
        print("3. Analyze Snort Logs")
        print("4. Dashboard")
        print("5. Generate Report")
        print("6. Exit")

        choice = input("\nEnter Choice : ")

        if choice == "1":

            host = input("Host/IP : ")
            start = int(input("Start Port : "))
            end = int(input("End Port : "))

            scan_ports(host, start, end)

        elif choice == "2":

            monitor_network()

        elif choice == "3":

            analyze_logs()

        elif choice == "4":

            dashboard()

        elif choice == "5":

            generate_report()

        elif choice == "6":

            print("Exiting...")
            break

        else:
            print("Invalid Choice")
if __name__ == "__main__":
    menu()
