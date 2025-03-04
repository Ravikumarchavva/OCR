import requests
import os
from dotenv import load_dotenv
load_dotenv()

SERVER_IP = os.getenv("SERVER_IP")
OWN_IP = '127.0.0.1'

def send_invoice(file_path):
    # url = f"http://{SERVER_IP}:8000/extract-invoice/"
    url = f"http://{OWN_IP}:8000/extract-invoice/"
    timeout = 300
    response = None
    with open(file_path, 'rb') as f:
        files = {'filename': (os.path.basename(file_path), f, 'application/pdf')}
        try:
            response = requests.post(url, files=files, timeout=timeout)
            response.raise_for_status()
            print(response.text)
        except requests.exceptions.RequestException as e:
            print(f"Error while calling API: {e}")
            if response is not None:
                print(f"Status Code: {response.status_code}")
                print(f"Response Body: {response.text}")

# Example usage
if __name__ == "__main__":
    file_path = "data/invoices/PerfectMatch.pdf"
    send_invoice(file_path)
