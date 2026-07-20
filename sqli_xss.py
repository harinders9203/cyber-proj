import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class WebVulnerabilityScanner:

    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    # -----------------------------
    # Get all forms from webpage
    # -----------------------------
    def get_forms(self):
        try:
            response = self.session.get(self.url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            return soup.find_all("form")
        except Exception as e:
            print("[-] Error:", e)
            return []

    # -----------------------------
    # Extract form details
    # -----------------------------
    def form_details(self, form):

        details = {}

        action = form.attrs.get("action", "")
        method = form.attrs.get("method", "get").lower()

        inputs = []

        for tag in form.find_all("input"):
            inputs.append({
                "type": tag.attrs.get("type", "text"),
                "name": tag.attrs.get("name"),
                "value": tag.attrs.get("value", "")
            })

        details["action"] = action
        details["method"] = method
        details["inputs"] = inputs

        return details

    # -----------------------------
    # Submit form
    # -----------------------------
    def submit_form(self, details, value):

        target = urljoin(self.url, details["action"])

        data = {}

        for input_tag in details["inputs"]:

            if input_tag["type"] in ["text", "search", "email", "password"]:
                data[input_tag["name"]] = value

            elif input_tag["value"]:
                data[input_tag["name"]] = input_tag["value"]

        if details["method"] == "post":
            return self.session.post(target, data=data)

        return self.session.get(target, params=data)

    # -----------------------------
    # SQL Injection Checker
    # -----------------------------
    def check_sqli(self):

        print("\n========== SQL Injection Scan ==========")

        payloads = [
            "'",
            "\"",
            "' OR '1'='1",
            "\" OR \"1\"=\"1"
        ]

        errors = [
            "sql syntax",
            "mysql",
            "warning",
            "sqlite",
            "postgresql",
            "oracle",
            "syntax error",
            "unclosed quotation mark",
            "odbc",
            "mysqli"
        ]

        forms = self.get_forms()

        if len(forms) == 0:
            print("No forms found.")
            return

        for form in forms:

            details = self.form_details(form)

            for payload in payloads:

                response = self.submit_form(details, payload)

                text = response.text.lower()

                for error in errors:

                    if error in text:

                        print("[+] Possible SQL Injection Found")
                        print("Payload :", payload)
                        print("Action  :", details["action"])
                        print("Method  :", details["method"])
                        return

        print("[-] No SQL Injection indicators detected.")

    # -----------------------------
    # XSS Checker
    # -----------------------------
    def check_xss(self):

        print("\n========== XSS Scan ==========")

        payload = "<script>alert('XSS')</script>"

        forms = self.get_forms()

        if len(forms) == 0:
            print("No forms found.")
            return

        for form in forms:

            details = self.form_details(form)

            response = self.submit_form(details, payload)

            if payload in response.text:

                print("[+] Possible Reflected XSS Found")
                print("Action :", details["action"])
                print("Method :", details["method"])
                return

        print("[-] No Reflected XSS detected.")


# =====================================
# Main
# =====================================

if __name__ == "__main__":

    target = input("Enter Target URL : ")

    scanner = WebVulnerabilityScanner(target)

    scanner.check_sqli()
    scanner.check_xss()