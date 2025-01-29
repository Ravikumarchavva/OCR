from tqdm.auto import tqdm 
from IPython.display import display, HTML
from json2html import json2html
import json
import re
import base64


class Invoice:
    def __init__(self, data):
        self.data = data
    
    def __getitem__(self, key):
        return self.data[key]
    
class InvoiceExtractor:

    def __init__(self, model):
        self.model = model

    @staticmethod
    def transform_pdf(file_path):
        with open(file_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()
        return base64.standard_b64encode(pdf_data).decode("utf-8")
    
    @staticmethod
    def extract_json(response_text):
        """Extracts JSON data from model response."""
        match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise ValueError("No valid JSON found in response")

    def extract(self, pdf_path):
        encoded_pdf = self.transform_pdf(pdf_path)
        prompt = "Extract invoice details from the file . and write as json"

        response = self.model.generate_content(
            [{'mime_type': 'application/pdf', 'data': encoded_pdf},
            prompt]
        )

        response_text = response.text
        invoice_data = self.extract_json(response_text)

        return Invoice(invoice_data)
    
    def extract_all(self, pdf_dir, limit=None):
        invoices = []
        pdfs = list(pdf_dir.glob("*.pdf"))
        len_pdfs = len(pdfs)
        if limit:
            if limit > len_pdfs:
                limit = len_pdfs
            pdfs = pdfs[:limit]      
              
        for pdf_path in tqdm(pdfs):
            invoice = self.extract(pdf_path)
            invoices.append(invoice)
        return invoices
    
    @staticmethod
    def display(invoice):
        html_table = json2html.convert(json=invoice.data)
        display(HTML(html_table))

    def display_all(self, invoices):
        for invoice in invoices:
            self.display(invoice)
            print("\n")

    @staticmethod
    def save(invoice, output_dir):
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{invoice['invoice_no']}.json"
        with open(output_path, "w") as output_file:
            json.dump(invoice.data, output_file, indent=2)

    def save_all(self, invoices, output_dir):
        for invoice in invoices:
            self.save(invoice, output_dir)