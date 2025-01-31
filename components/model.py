import google.generativeai as genai
import os
import sys
from IPython.display import display, HTML
from json2html import json2html

from dotenv import load_dotenv
load_dotenv()
GCP_KEY = os.getenv("GCP_KEY")

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from configs import PROMPT
from components.extractor import InvoiceExtractor

class OCR_Model:
    def __init__(self, model="gemini-2.0-flash-exp"):
        genai.configure(api_key=GCP_KEY)
        self.model = genai.GenerativeModel(model)

    def predict(self, data):
        response = self.model.generate_content(
            [{"mime_type": "application/pdf", "data": data}, PROMPT]
        )
        return response.text

    def extract(self, data):
        response_text = self.predict(data)
        extractor = InvoiceExtractor()
        return extractor.extract(response_text)

    def display(self, invoice, html=False):
        if html:
            html_table = json2html.convert(json=invoice.data)
            display(HTML(html_table))
        else:
            display(invoice.data)