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
        transformed_pdf = self.transform_pdf(pdf_path)
        prompt = (
                "Extract structured invoice details from this PDF. Return all fields exactly as they appear in the document. "
                "Follow this strict JSON format:\n"
                "{\n"
                '    "line_items": [\n'
                '        {\n'
                '            "description": "string",\n'
                '            "quantity": string,\n'
                '            "price_per_unit": string,\n'
                '            "vat_percent": string,\n'
                '            "total_price": string\n'
                '        }\n'
                '    ],\n'
                '    "total_amount": {\n'
                '        "total_items": number,\n'
                '        "total_tax": string,\n'
                '        "total_price": string\n'
                '    },\n'
                '    "due_date": "YYYY-MM-DD",\n'
                '    "payment_date": "YYYY-MM-DD",\n'
                '    "invoice_date": "YYYY-MM-DD",\n'
                '    "invoice_number": "string",\n'
                '    "purchase_order": "string",\n'
                '    "reference_numbers": ["string"],\n'
                '    "locale": "string",\n'
                '    "country": "string",\n'
                '    "currency": "string",\n'
                '    "payment_details": {\n'
                '        "iban": "string",\n'
                '        "swift": "string",\n'
                '        "bic": "string",\n'
                '        "account_number": "string"\n'
                '    },\n'
                '    "supplier_company_registrations": {\n'
                '        "siret": "string",\n'
                '        "ein": "string",\n'
                '        "vat_number": "string"\n'
                '    },\n'
                '    "supplier_name": "string",\n'
                '    "total_tax": string,\n'
                '    "taxes_details": [\n'
                '        {\n'
                '            "rate": string,\n'
                '            "amount": string\n'
                '        }\n'
                '    ],\n'
                '    "total_amount_including_taxes": string,\n'
                '    "total_net_amount_excluding_taxes": string,\n'
                '    "customer_address": "string",\n'
                '    "shipping_address": "string",\n'
                '    "billing_address": "string",\n'
                '    "customer_company_registrations": {\n'
                '        "vat_number": "string"\n'
                '    },\n'
                '    "customer_name": "string",\n'
                '    "supplier_address": "string"\n'
                '}\n\n'
                "Rules:\n"
                "- Retain the original number formatting exactly as it appears in the document, including decimal and thousand separators.\n"
                "- Ensure **all numbers match exactly** as in the document.\n"
                "- If any field is missing, return `null` rather than removing it.\n"
                "- DO NOT add extra details.\n"
                "- If items have any charges, also write them in line items—DO NOT skip.\n"
            )

        # prompt = "extract invoice details from this PDF file in JSON format"

        response = self.model.generate_content([{
                        'mime_type': 'application/pdf',
                        'data': transformed_pdf
                    },prompt])

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