import socket
import time
PORT_INFO = {
    21: {
        "service": "FTP",
        "attacks": [
            "Brute-force login attempts",
            "Anonymous access abuse",
            "Credential theft"
        ],
        "security": [
            "Disable anonymous login",
            "Use SFTP/FTPS",
            "Use strong passwords"
        ]
    },

    22: {
        "service": "SSH",
        "attacks": [
            "Brute-force authentication",
            "Credential stuffing",
            "Outdated software vulnerabilities"
        ],
        "security": [
            "Use SSH keys",
            "Disable root login",
            "Restrict access with firewall"
        ]
    },

    23: {
        "service": "Telnet",
        "attacks": [
            "Credential sniffing",
            "Unauthorized remote access"
        ],
        "security": [
            "Disable Telnet",
            "Replace with SSH"
        ]
    },

    80: {
        "service": "HTTP",
        "attacks": [
            "Web application attacks",
            "Directory enumeration",
            "Misconfiguration abuse"
        ],
        "security": [
            "Keep web applications updated",
            "Use HTTPS",
            "Apply security headers"
        ]
    },

    443: {
        "service": "HTTPS",
        "attacks": [
            "TLS misconfiguration",
            "Web application attacks"
        ],
        "security": [
            "Use modern TLS",
            "Keep certificates valid",
            "Patch web applications"
        ]
    },

    3306: {
        "service": "MySQL",
        "attacks": [
            "Weak credential abuse",
            "Unauthorized database access"
        ],
        "security": [
            "Bind to localhost",
            "Use firewall",
            "Strong passwords"
        ]
    },

    3389: {
        "service": "RDP",
        "attacks": [
            "Password guessing",
            "Credential theft"
        ],
        "security": [
            "Enable MFA",
            "Use VPN",
            "Enable Network Level Authentication"
        ]
    }
}


host = input("Enter website or IP: ")

try:
    ip = socket.gethostbyname(host)
except:
    print("Invalid Host")
    exit()

start = int(input("Start Port: "))
end = int(input("End Port: "))

print(f"\nScanning {host} ({ip})...\n")

scan_start = time.time()

for port in range(start, end + 1):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    result = sock.connect_ex((ip, port))

    if result == 0:

        print("=" * 55)
        print(f"PORT : {port}")

        if port in PORT_INFO:

            info = PORT_INFO[port]

            print("STATUS  : OPEN")
            print("SERVICE :", info["service"])

            print("\nCommon Attack Categories:")
            for attack in info["attacks"]:
                print(" -", attack)

            print("\nRecommended Security:")
            for item in info["security"]:
                print(" +", item)

        else:

            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"

            print("STATUS  : OPEN")
            print("SERVICE :", service)
            print("No security profile available.")

    sock.close()

print("\nScan Completed")
print("Time:", round(time.time() - scan_start, 2), "seconds")