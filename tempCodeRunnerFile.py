import socket
import time
import os
from collections import Counter

# GLOBAL DATA
alerts = []
open_ports = []
packet_count = Counter()

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


def monitor_network(seconds=5):

    print("\nMonitoring Network...")

    try:

        s = socket.socket(
            socket.AF_INET,
            socket.SOCK_RAW,
            socket.IPPROTO_IP
        )

        host = socket.gethostbyname(socket.gethostname())

        s.bind((host, 0))

        s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        start = time.time()

        while time.time() - start < seconds:

            packet = s.recvfrom(65565)

            packet_count["Packets"] += 1

        s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

    except Exception:

        print("Raw socket requires Administrator/Root privileges.")

# SNORT LOG ANALYZER


def analyze_logs(file_name="alerts.log"):

    print("\nReading Snort Logs...\n")

    if not os.path.exists(file_name):

        print("No alerts.log found")
        return

    with open(file_name, "r", errors="ignore") as f:

        for line in f:

            if "SCAN" in line.upper():
                alerts.append(("Medium", "Port Scan"))

            elif "SQL" in line.upper():
                alerts.append(("High", "SQL Injection Attempt"))

            elif "BRUTE" in line.upper():
                alerts.append(("High", "Brute Force"))

            elif "SSH" in line.upper():
                alerts.append(("Medium", "SSH Activity"))

            else:
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