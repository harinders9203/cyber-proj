import socket
import hashlib
import os
import re
from datetime import datetime

captured_packets = []
MAX_STORED_PACKETS = 500

# PORT SCANNER

def port_scanner():
    host = input("Enter Host/IP: ")

    try:
        ip = socket.gethostbyname(host)
    except:
        print("Invalid Host")
        return

    start = int(input("Start Port: "))
    end = int(input("End Port: "))

    print(f"\nScanning {host} ({ip})...\n")

    for port in range(start, end + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)

        if s.connect_ex((ip, port)) == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"

            print(f"Port {port} : OPEN ({service})")

        s.close()



# DNS/IP LOOKUP

def dns_lookup():
    domain = input("Enter Domain: ")

    try:
        ip = socket.gethostbyname(domain)
        print("IP Address :", ip)

        try:
            host = socket.gethostbyaddr(ip)
            print("Reverse DNS :", host[0])
        except:
            print("Reverse DNS : Not Available")

    except:
        print("Invalid Domain")

# WEB SECURITY CHECKER
def web_security_checker():
    print("\nBasic Web Security Checklist")
    print("- HTTPS enabled?")
    print("- Security headers present?")
    print("- Input validation implemented?")
    print("- Software kept up to date?")
    print("\nThis module is a checklist only.")


# PASSWORD STRENGTH

def password_checker():

    password = input("Enter Password: ")

    score = 0

    if len(password) >= 8:
        score += 1

    if re.search(r"[A-Z]", password):
        score += 1

    if re.search(r"[a-z]", password):
        score += 1

    if re.search(r"[0-9]", password):
        score += 1

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1

    if score <= 2:
        strength = "Weak"
    elif score == 3:
        strength = "Medium"
    else:
        strength = "Strong"

    print("Password Strength :", strength)

# HASH GENERATOR

def hash_generator():

    text = input("Enter Text: ")

    print("\nMD5     :", hashlib.md5(text.encode()).hexdigest())
    print("SHA1    :", hashlib.sha1(text.encode()).hexdigest())
    print("SHA256  :", hashlib.sha256(text.encode()).hexdigest())
    print("SHA512  :", hashlib.sha512(text.encode()).hexdigest())

# FILE METADATA
def metadata_analyzer():

    path = input("Enter File Path: ")

    if not os.path.exists(path):
        print("File Not Found")
        return

    print("\nFilename :", os.path.basename(path))
    print("Size     :", os.path.getsize(path), "bytes")
    print("Created  :", os.path.getctime(path))
    print("Modified :", os.path.getmtime(path))

# PACKET SNIFFER

try:
    from scapy.all import sniff, conf
except ImportError:
    sniff = None
    conf = None

def summarize_packet(packet):

    summary = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "src_ip": "N/A",
        "dst_ip": "N/A",
        "protocol": "Other",
        "src_port": "N/A",
        "dst_port": "N/A",
        "size": len(packet),
    }

    if packet.haslayer("IP"):
        summary["src_ip"] = packet["IP"].src
        summary["dst_ip"] = packet["IP"].dst

    if packet.haslayer("TCP"):
        summary["protocol"] = "TCP"
        summary["src_port"] = packet["TCP"].sport
        summary["dst_port"] = packet["TCP"].dport

    elif packet.haslayer("UDP"):
        summary["protocol"] = "UDP"
        summary["src_port"] = packet["UDP"].sport
        summary["dst_port"] = packet["UDP"].dport

    elif packet.haslayer("ICMP"):
        summary["protocol"] = "ICMP"

    return summary

def packet_callback(packet):

    summary = summarize_packet(packet)

    if len(captured_packets) >= MAX_STORED_PACKETS:
        captured_packets.pop(0)

    captured_packets.append(summary)

    print("\n" + "=" * 50)

    print("Timestamp      :", summary["timestamp"])
    print("Source IP      :", summary["src_ip"])
    print("Destination IP :", summary["dst_ip"])
    print("Protocol Name  :", summary["protocol"])
    print("Source Port    :", summary["src_port"])
    print("Destination Port:", summary["dst_port"])
    print("Packet Size    :", summary["size"], "bytes")

def start_sniffing():

    try:
        sniff(prn=packet_callback, store=False)
    except Exception as error:
        error_message = str(error).lower()
        needs_l3_fallback = (
            conf is not None and
            (
                "layer 2" in error_message or
                "winpcap" in error_message or
                "npcap" in error_message
            )
        )

        if not needs_l3_fallback:
            raise

        print("Layer 2 capture is unavailable. Falling back to Scapy's layer 3 socket...\n")
        sniff(prn=packet_callback, store=False, opened_socket=conf.L3socket())


def packet_sniffer():

    print("\nStarting Packet Sniffer...")
    print("Press Ctrl + C to stop.\n")

    if sniff is None:
        print("Scapy is not installed. Install it with: pip install scapy")
        return

    previous_count = len(captured_packets)

    try:
        start_sniffing()
    except KeyboardInterrupt:
        new_packets = len(captured_packets) - previous_count
        print(f"\nPacket capture stopped. Stored {new_packets} packet summaries.")
    except Exception as error:
        print(f"Packet sniffer error: {error}")
        print("If you want full packet capture on Windows, install Npcap from https://npcap.com/")


# PDF REPORT (TEXT REPORT)
def generate_report():

    report_path = "Security_Report.txt"

    with open(report_path, "w", encoding="utf-8") as file:
        file.write("CYBER SECURITY TOOLKIT REPORT\n")
        file.write("=============================\n")
        file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        file.write("Captured Packets Summary\n")
        file.write("------------------------\n")
        file.write(f"Stored Packets: {len(captured_packets)}\n\n")

        if not captured_packets:
            file.write("No packets have been captured yet.\n")
        else:
            for index, packet in enumerate(captured_packets, start=1):
                file.write(f"Packet {index}\n")
                file.write(f"  Timestamp        : {packet['timestamp']}\n")
                file.write(f"  Source IP        : {packet['src_ip']}\n")
                file.write(f"  Destination IP   : {packet['dst_ip']}\n")
                file.write(f"  Protocol         : {packet['protocol']}\n")
                file.write(f"  Source Port      : {packet['src_port']}\n")
                file.write(f"  Destination Port : {packet['dst_port']}\n")
                file.write(f"  Packet Size      : {packet['size']} bytes\n\n")

    print(f"Report Saved as {report_path}")

# MENU
def menu():

    while True:

        print("\n========== CYBER SECURITY TOOLKIT ==========")
        print("1. Port Scanner")
        print("2. DNS/IP Lookup")
        print("3. Web Security Checklist")
        print("4. Password Strength Checker")
        print("5. Hash Generator")
        print("6. File Metadata Analyzer")
        print("7. Packet Sniffer")
        print("8. Generate Report")
        print("9. Exit")

        choice = input("\nEnter Choice: ")

        if choice == "1":
            port_scanner()

        elif choice == "2":
            dns_lookup()

        elif choice == "3":
            web_security_checker()

        elif choice == "4":
            password_checker()

        elif choice == "5":
            hash_generator()

        elif choice == "6":
            metadata_analyzer()

        elif choice == "7":
            packet_sniffer()

        elif choice == "8":
            generate_report()

        elif choice == "9":
            print("Goodbye!")
            break

        else:
            print("Invalid Choice")



# MAIN
if __name__ == "__main__":
    menu()
