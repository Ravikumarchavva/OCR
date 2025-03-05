from google import genai
from google.genai import types
import os
import sys
from IPython.display import display, HTML
from json2html import json2html

from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from configs import PROMPT, RESPONSE_SCHEMA
from components.extractor import InvoiceExtractor


class OCR_Model:
    def __init__(self, model="gemini-2.0-flash-exp"):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

        self.model = model

    def _predict(self, data):
        """Generates response using the model."""
        response = self.client.models.generate_content(
            model=self.model,
            contents=[
                PROMPT,
                types.Part.from_bytes(data=data, mime_type="application/pdf"),
            ],
                # response_mime_type="application/json",
                # response_schema=RESPONSE_SCHEMA,
            config=types.GenerateContentConfig(
                temperature=0.001,
                max_output_tokens=50000,
            ),
        )
        return response.text

    def extract(self, data):
        """Extracts invoice data from the response."""
        response_text = self._predict(data)
        extractor = InvoiceExtractor()
        return extractor.extract(response_text)

    def display(self, invoice, html=False):
        """Displays the extracted invoice data."""
        if html:
            html_table = json2html.convert(json=invoice.data)
            display(HTML(html_table))
        else:
            display(invoice.data)
