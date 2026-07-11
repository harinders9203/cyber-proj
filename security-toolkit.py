import socket
import hashlib
import os
import re

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

# PACKET SNIFFER (PLACEHOLDER)

from scapy.all import sniff

def packet_callback(packet):

    print("\n" + "=" * 50)

    if packet.haslayer("IP"):

        print("Source IP      :", packet["IP"].src)
        print("Destination IP :", packet["IP"].dst)
        print("Protocol       :", packet["IP"].proto)

    if packet.haslayer("TCP"):
        print("Protocol Name  : TCP")
        print("Source Port    :", packet["TCP"].sport)
        print("Destination Port:", packet["TCP"].dport)

    elif packet.haslayer("UDP"):
        print("Protocol Name  : UDP")
        print("Source Port    :", packet["UDP"].sport)
        print("Destination Port:", packet["UDP"].dport)

    elif packet.haslayer("ICMP"):
        print("Protocol Name  : ICMP")

    print("Packet Size    :", len(packet), "bytes")


def packet_sniffer():

    print("\nStarting Packet Sniffer...")
    print("Press Ctrl + C to stop.\n")
    from scapy.all import sniff, conf

    sniff(
        prn=packet_callback,
        store=False,
        opened_socket=conf.L3socket()
    )


# PDF REPORT (TEXT REPORT)
def generate_report():

    with open("Security_Report.txt", "w") as file:
        file.write("CYBER SECURITY TOOLKIT REPORT\n")
        file.write("=============================\n")
        file.write("Report Generated Successfully.\n")

    print("Report Saved as Security_Report.txt")

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
menu()