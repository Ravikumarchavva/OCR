from pathlib import Path

ROOT_DIR = Path(__file__).parent

PROMPT = (
    "Extract structured invoice details from this PDF. Return all fields exactly as they appear in the document. "
    "Follow this strict JSON format:\n"
    "{\n"
    '    "line_items": [\n'
    "        {\n"
    '            "product_code": "string",\n'
    '            "description": "string",\n'
    '            "quantity": string,\n'
    '            "price_per_unit": string,\n'
    '            "vat_percent": string,\n'
    '            "total_price": string\n'
    "        }\n"
    "    ],\n"
    '    "total_amount": {\n'
    '        "total_items": number,\n'
    '        "total_tax": string,\n'
    '        "total_price": string\n'
    "    },\n"
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
    "    },\n"
    '    "vat_number": "string"\n'
    '    "supplier_name": "string",\n'
    '    "taxes_details": [\n'
    "        {\n"
    '            "rate": string,\n'
    '            "amount": string\n'
    "        }\n"
    "    ],\n"
    '    "total_amount_including_taxes": string,\n'
    '    "total_net_amount_excluding_taxes": string,\n'
    '    "customer_address": "string",\n'
    '    "shipping_address": "string",\n'
    '    "billing_address": "string",\n'
    '    "customer_company_registrations": {\n'
    '        "vat_number": "string"\n'
    "    },\n"
    '    "customer_name": "string",\n'
    '    "supplier_address": "string"\n'
    "}\n\n"
    "Rules:\n"
    "- Retain the original number formatting exactly as it appears in the document, including decimal and thousand separators.\n"
    "- Ensure **all numbers match exactly** as in the document.\n"
    "- If any field is missing, return `null` rather than removing it.\n"
    "- DO NOT add extra details.\n"
    "- If items have any charges, also write them in line items—DO NOT skip.\n"
    "- If the due_date is not provided but the number of due days is available, calculate the due date manullay from invoice date and due days available.\n"  # resource exhusting
)

# MODEL = "gemini-2.0-flash-exp"

MODEL = "gemini-2.0-flash-thinking-exp-01-21"