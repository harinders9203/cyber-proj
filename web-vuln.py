import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

requests.packages.urllib3.disable_warnings()

results = {}

def banner():
    print("=" * 50)
    print("      WEBSITE SECURITY AUDIT TOOL")
    print("=" * 50)


def get_url():
    url = input("Enter Website URL (https://example.com): ").strip()

    if not url.startswith("http"):
        url = "https://" + url

    return url


def check_https(url):
    print("\n[HTTPS CHECK]")
    if url.startswith("https://"):
        print("[+] HTTPS is enabled")
        results["HTTPS"] = "Enabled"
    else:
        print("[-] HTTPS is not enabled")
        results["HTTPS"] = "Disabled"


def check_headers(url):
    print("\n[SECURITY HEADERS]")

    try:
        r = requests.get(url, timeout=5, verify=False)

        headers = [
            "Content-Security-Policy",
            "Strict-Transport-Security",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Referrer-Policy"
        ]

        for h in headers:
            if h in r.headers:
                print(f"[+] {h}")
                results[h] = "Present"
            else:
                print(f"[-] {h}")
                results[h] = "Missing"

    except Exception as e:
        print(e)


def check_server(url):
    print("\n[SERVER INFO]")

    try:
        r = requests.get(url, timeout=5, verify=False)

        server = r.headers.get("Server", "Hidden")
        powered = r.headers.get("X-Powered-By", "Hidden")

        print("Server:", server)
        print("Powered By:", powered)

        results["Server"] = server
        results["Powered By"] = powered

    except Exception as e:
        print(e)


def check_cookies(url):
    print("\n[COOKIE SECURITY]")

    try:
        r = requests.get(url, timeout=5, verify=False)

        if not r.cookies:
            print("No cookies found.")
            return

        for cookie in r.cookies:
            print("Cookie:", cookie.name)

        results["Cookies"] = len(r.cookies)

    except Exception as e:
        print(e)


def check_robots(url):
    print("\n[ROBOTS.TXT]")

    try:
        robot = urljoin(url, "/robots.txt")

        r = requests.get(robot, timeout=5, verify=False)

        if r.status_code == 200:
            print("[+] robots.txt found")
            results["robots.txt"] = "Found"
        else:
            print("[-] robots.txt not found")
            results["robots.txt"] = "Not Found"

    except Exception as e:
        print(e)


def check_sitemap(url):
    print("\n[SITEMAP]")

    try:
        sitemap = urljoin(url, "/sitemap.xml")

        r = requests.get(sitemap, timeout=5, verify=False)

        if r.status_code == 200:
            print("[+] sitemap.xml found")
            results["sitemap"] = "Found"
        else:
            print("[-] sitemap.xml not found")
            results["sitemap"] = "Not Found"

    except Exception as e:
        print(e)


def detect_forms(url):
    print("\n[HTML FORMS]")

    try:
        r = requests.get(url, timeout=5, verify=False)

        soup = BeautifulSoup(r.text, "html.parser")

        forms = soup.find_all("form")

        print("Forms Found:", len(forms))

        results["Forms"] = len(forms)

    except Exception as e:
        print(e)


def check_http_options(url):
    print("\n[HTTP METHODS]")

    try:
        r = requests.options(url, timeout=5, verify=False)

        methods = r.headers.get("Allow", "Unknown")

        print("Allowed Methods:", methods)

        results["Methods"] = methods

    except Exception as e:
        print(e)


def summary():
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)

    for key, value in results.items():
        print(f"{key:30} : {value}")

    print("=" * 50)


def menu():

    url = get_url()

    while True:

        print("""
1. HTTPS Check
2. Security Headers
3. Server Information
4. Cookie Check
5. robots.txt
6. sitemap.xml
7. Detect Forms
8. HTTP Methods
9. Full Scan
10. Show Summary
0. Exit
""")

        choice = input("Select Option: ")

        if choice == "1":
            check_https(url)

        elif choice == "2":
            check_headers(url)

        elif choice == "3":
            check_server(url)

        elif choice == "4":
            check_cookies(url)

        elif choice == "5":
            check_robots(url)

        elif choice == "6":
            check_sitemap(url)

        elif choice == "7":
            detect_forms(url)

        elif choice == "8":
            check_http_options(url)

        elif choice == "9":
            check_https(url)
            check_headers(url)
            check_server(url)
            check_cookies(url)
            check_robots(url)
            check_sitemap(url)
            detect_forms(url)
            check_http_options(url)
            summary()

        elif choice == "10":
            summary()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid Option")


if __name__ == "__main__":
    banner()
    menu()