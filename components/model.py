import google.generativeai as genai
import os
import sys
from IPython.display import display, HTML
from json2html import json2html

from dotenv import load_dotenv
load_dotenv()
GCP_KEY = os.getenv("GCP_KEY")

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from configs import PROMPT, MODEL, MODEL_CONFIG
from components.extractor import InvoiceExtractor

class OCR_Model:
    def __init__(self, model=MODEL):
        genai.configure(api_key=GCP_KEY)
        self.model = genai.GenerativeModel(model)
        genai.GenerationConfig(MODEL_CONFIG)

    def _predict(self, data):
        '''Generates response using the model.'''
        response = self.model.generate_content(
            [{"mime_type": "application/pdf", "data": data}, PROMPT],
        )
        return response.text

    def extract(self, data):
        '''Extracts invoice data from the response.'''
        response_text = self._predict(data)
        extractor = InvoiceExtractor()
        return extractor.extract(response_text)

    def display(self, invoice, html=False):
        '''Displays the extracted invoice data.'''
        if html:
            html_table = json2html.convert(json=invoice.data)
            display(HTML(html_table))
        else:
            display(invoice.data)