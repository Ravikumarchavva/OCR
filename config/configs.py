from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

PROMPT = (
    "Extract structured invoice details from this PDF. Return all fields exactly as they appear in the document. "
    "Follow this strict JSON format:\n"
    "{\n"
    '    "line_items": [\n'
    "        {\n"
    '            "product_code": "string",\n'
    '            "description": "string",\n'
    '            "quantity": "string",\n'
    '            "price_per_unit": "string",\n'
    '            "vat_percent": "string",\n'
    '            "total_price": "string"\n'
    "        }\n"
    "    ],\n"
    '    "total_amount": {\n'
    '        "total_items": number,\n'
    '        "total_tax": "string",\n'
    '        "total_price": "string"\n'
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
    '    "vat_number": "string",\n'
    '    "supplier_name": "string",\n'
    '    "taxes_details": [\n'
    "        {\n"
    '            "rate": "string",\n'
    '            "amount": "string"\n'
    "        }\n"
    "    ],\n"
    '    "total_amount_including_taxes": "string",\n'
    '    "total_net_amount_excluding_taxes": "string",\n'
    '    "customer_address": "string",\n'
    '    "shipping_address": "string",\n'
    '    "billing_address": "string",\n'
    '    "customer_company_registrations": {\n'
    '        "vat_number": "string"\n'
    "    },\n"
    '    "customer_name": "string",\n'
    '    "supplier_address": "string"\n'
    "}\n\n"
    "### Instructions for Invoice Extraction\n"
    "1. **Document Analysis:**\n"
    "   - Thoroughly scan the entire invoice to identify key sections such as the header, line items, summary totals, tax details, payment instructions, and addresses.\n"
    "   - Recognize and extract fields like invoice number, invoice date, due date (or compute it using provided due days), payment date, supplier and customer information, and purchase orders.\n\n"
    "2. **Line Items Extraction:**\n"
    "   - For each line item, extract the following fields exactly as they appear:\n"
    "     - **Product Code:** The unique alphanumeric identifier.\n"
    "     - **Description:** A precise description of the item.\n"
    "     - **Quantity:** Maintain the original formatting (including decimals, thousand separators, etc.).\n"
    "     - **Price Per Unit:** Capture the exact price formatting.\n"
    "     - **VAT Percent:** The tax rate applied to the item.\n"
    "     - **Total Price:** The total price for the line, preserving the document's number format.\n"
    "   - **Note:** Do not omit any charge-related entries (such as shipping, handling, or service fees). If any field is missing, assign a value of `null`.\n\n"
    "3. **Totals and Taxes:**\n"
    "   - Extract summary totals, including total tax, total price, and the overall amount. If the document specifies due days instead of an explicit due date, compute the due date using the invoice date plus the due days.\n"
    "   - Extract detailed tax breakdowns where available, ensuring that the rate and corresponding amount are exactly as stated.\n\n"
    "4. **Dates Processing:**\n"
    "   - Precisely capture dates such as invoice date, due date, and payment date. You may find this in many ways like `payment terms`, `payment conditions` etc saying like `within X days`, `X days from date of INVOICE` or similar. If a due date is not directly provided but 'due in X days' is indicated, calculate it by adding X days to the invoice date.\n\n"
    "5. **Payment and Banking Details:**\n"
    "   - Extract all available payment details including IBAN, SWIFT, BIC, and account number. Return `null` for any missing banking fields.\n\n"
    "6. **Supplier and Customer Information:**\n"
    "   - Extract supplier and customer names, addresses (billing, shipping, and customer addresses), and any company registration or VAT numbers. Ensure that the extracted text matches the source document exactly.\n\n"
    "7. **Final Output Requirements:**\n"
    "   - The final JSON must adhere strictly to the provided format. All numbers, including decimals and thousand separators, must be preserved exactly as they appear in the document.\n"
    "   - No additional fields or assumptions should be included beyond what is explicitly provided in the invoice.\n"
    "   - For any field that is not found, return a `null` value rather than omitting the field.\n"
)

# MODEL = "gemini-1.5-flash"

# MODEL = 'gemini-1.5-pro'

# MODEL = "gemini-2.0-flash-exp"

# MODEL = "gemini-2.0-flash-thinking-exp-1219"

MODEL = "gemini-2.0-flash-thinking-exp-01-21"

MODEL_CONFIG = {
    "stopSequences": ["### End of Invoice ###"],
    "responseMimeType": "application/json",
    "temperature": 0.3,
    "topP": 0.8,
    "topK": 40,
    "candidateCount": 1,
    "maxOutputTokens": 30000,
    "seed": 42,
}
