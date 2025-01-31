import re
import json
from components.invoice import Invoice

class InvoiceExtractor:
    def __init__(self):
        pass

    def extract(self, response_text):
        '''Extracts JSON data from model response.'''
        match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if match:
            extracted_data = json.loads(match.group(0))
            return Invoice(extracted_data)
        raise ValueError("No valid JSON found in response")

