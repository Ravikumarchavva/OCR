import re
import json
from components.invoice import Invoice

class InvoiceExtractor:
    def __init__(self):
        pass

    def extract(self, response_text):
        '''Extracts and merges JSON data from model response using balanced brace parsing.'''
        def extract_json_objects(text):
            objs = []
            brace_count = 0
            start = None
            for i, ch in enumerate(text):
                if ch == '{':
                    if brace_count == 0:
                        start = i
                    brace_count += 1
                elif ch == '}':
                    brace_count -= 1
                    if brace_count == 0 and start is not None:
                        objs.append(text[start:i+1])
            return objs

        json_blocks = extract_json_objects(response_text)
        if not json_blocks:
            raise ValueError("No valid JSON found in response")
        combined_data = {}
        for block in json_blocks:
            data = json.loads(block)
            combined_data.update(data)
        return Invoice(combined_data)

