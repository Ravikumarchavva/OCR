import requests
import os
import sys
from dotenv import load_dotenv
from src.logger import AppLogger
load_dotenv()

SERVER_IP = os.getenv("SERVER_IP")
OWN_IP = '127.0.0.1'

def send_invoice(file_path, IP):
    url = f"http://{IP}:8000/extract-invoice/"
    timeout = 300
    response = None
    with open(file_path, 'rb') as f:
        files = {'filename': (os.path.basename(file_path), f, 'application/pdf')}
        try:
            response = requests.post(url, files=files, timeout=timeout)
            response.raise_for_status()
            print(response.text)
        except requests.exceptions.RequestException as e:
            AppLogger.log_exception(sys.exc_info())
            if response is not None:
                print(f"Status Code: {response.status_code}")
                print(f"Response Body: {response.text}")

# Example usage
if __name__ == "__main__":
    file_path = "data/invoices/Invoice.pdf"
    SERVER = input("Select IP : server or localhost: ")
    if SERVER == 'server':
        send_invoice(file_path, SERVER_IP)
    elif SERVER == 'localhost':
        send_invoice(file_path, OWN_IP)
    else:
        print("Invalid input")
