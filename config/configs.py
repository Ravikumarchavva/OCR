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

REPORT_PROMPT = (
    "You are a quality control report extractor. Your task is to extract structured quality control details from the "
    "provided page text and output a valid JSON object conforming to the given schema.\n\n"
    "### **Required Fields and Their Meanings:**\n"
    "- **product_name** (string): The name of the product.\n"
    "- **RAG** (string): The RAG value (e.g., \"BLUE\", \"AMBER\", \"GREEN\").\n"
    "- **expected_qty** (string): The expected quantity.\n"
    "- **received_qty** (string): The received quantity.\n"
    "- **supplier_code** (string): The supplier code.\n"
    "- **supplier** (string): The supplier name.\n"
    "- **coo** (string): Country of Origin.\n"
    "- **received_date** (string): Date/time when received, in \"YYYY-MM-DD HH:MM:SS\" format.\n"
    "- **inspection_date** (string): Date/time of inspection, in \"YYYY-MM-DD HH:MM:SS\" format.\n"
    "- **print_date** (string): The print date, in \"YYYY-MM-DD\" format.\n"
    "- **iss_pallet_id** (string): ISS Pallet ID.\n"
    "- **supplier_pallet_id** (string): Supplier Pallet ID.\n"
    "- **customer_pallet_id** (string): Customer Pallet ID.\n"
    "- **variety** (string): The variety of the product.\n"
    "- **brand** (string): The brand name.\n"
    "- **organic** (string): \"YES\" or \"NO\" if the product is organic.\n"
    "- **does_pallet_meet_spec** (string): \"YES\" or \"NO\" if the pallet meets specifications.\n"
    "- **end_customer** (string): The end customer.\n"
    "- **harvest_date** (string): The date the product was harvested, in \"YYYY-MM-DD\" format.\n"
    "- **dp** (string): The DP code.\n"
    "- **total_defects** (integer): Total defects.\n"
    "- **size_calibre** (string): Size calibre.\n"
    "- **lot_number** (string): The lot number.\n"
    "- **inspector** (string): The inspector's name.\n"
    "- **estimated_yield** (string): Estimated yield.\n"
    "- **defects_tot** (integer): Total number of defects.\n"
    "- **defects_fruit_total** (integer): Total defects in the fruit.\n"
    "- **packs_with_defects** (integer): Number of packs with defects.\n"
    "- **waste_tot** (integer): Total waste.\n"
    "- **waste_fruit_total** (integer): Fruit waste.\n"
    "- **packs_with_waste** (integer): Number of packs with waste.\n"
    "- **minor_defects_tot** (integer): Total minor defects.\n"
    "- **minor_fruit_total** (integer): Minor defects in the fruit.\n"
    "- **major_defects_tot** (integer): Total major defects.\n"
    "- **major_fruit_total** (integer): Major defects in the fruit.\n"
    "- **packs_with_major** (integer): Number of packs with major defects.\n"
    "- **box_pack_weights** (string): The box pack weights.\n"
    "- **weight_readings** (string): Weight readings recorded.\n"
    "- **fruit_weights** (string): The fruit weights.\n"
    "- **qa_comments** (string): Any QA comments.\n"
    "- **packs_fruits_inspected_sample_size** (integer): The sample size for inspection.\n"
    "- **boxes_inspected** (integer): Number of boxes inspected.\n"
    "- **c** (string): Additional info.\n\n"
    "### **Extraction Rules:**\n"
    "- **Do NOT infer values** from unrelated text.\n"
    "- **If a field is not found,** set it to **null**.\n"
    "- **Extract exactly as they appear** in the text.\n"
    "- If you find empty space after any key, return `null` for that key.\n\n"
    "### **QC Report Page Text:**\n"
    "### **Example of Correct Output:**\n"
    "```json\n"
    "{\n"
    "    \"product_name\": \"Cucumbers 18 Loose\",\n"
    "    \"RAG\": \"BLUE\",\n"
    "    \"expected_qty\": \"150\",\n"
    "    \"received_qty\": \"150\",\n"
    "    \"supplier_code\": \"GNK€\",\n"
    "    \"supplier\": \"G.GIANNAKAKIS SA\",\n"
    "    \"coo\": \"Greece\",\n"
    "    \"received_date\": \"19/01/2025 08:15:09\",\n"
    "    \"inspection_date\": \"19/01/2025 12:32:00\",\n"
    "    \"print_date\": \"19/01/2025\",\n"
    "    \"iss_pallet_id\": \"6194840\",\n"
    "    \"supplier_pallet_id\": \"6194840\",\n"
    "    \"customer_pallet_id\": null,\n"
    "    \"variety\": \"Not Available\",\n"
    "    \"brand\": \"LSEEX\",\n"
    "    \"organic\": \"NO\",\n"
    "    \"does_pallet_meet_spec\": \"YES\",\n"
    "    \"end_customer\": \"Tesco\",\n"
    "    \"harvest_date\": \"19/01/2025\",\n"
    "    \"dp\": \"51\",\n"
    "    \"total_defects\": \"5.56%\",\n"
    "    \"size_calibre\": null,\n"
    "    \"lot_number\": \"676779\",\n"
    "    \"inspector\": \"Marzena.Buslowicz\",\n"
    "    \"estimated_yield\": \"100.00%\",\n"
    "    \"defects_tot\": \"5.56%\",\n"
    "    \"defects_fruit_total\": \"6.00\",\n"
    "    \"packs_with_defects\": \"4.63%\",\n"
    "    \"waste_tot\": \"0.00%\",\n"
    "    \"waste_fruit_total\": \"0.00\",\n"
    "    \"packs_with_waste\": \"0\",\n"
    "    \"minor_defects_tot\": \"4.63%\",\n"
    "    \"minor_fruit_total\": \"6.00\",\n"
    "    \"major_defects_tot\": \"0.00%\",\n"
    "    \"major_fruit_total\": \"0.00\",\n"
    "    \"packs_with_major\": \"0\",\n"
    "    \"box_pack_weights\": \"Avg 279g; Min 264g; Max 308g\",\n"
    "    \"weight_readings\": \"264 267 269 276 277 281 282 284 286 308\",\n"
    "    \"fruit_weights\": \"Avg 0.00g\",\n"
    "    \"qa_comments\": \"No major issues, flowering and untidy wrap present.\",\n"
    "    \"packs_fruits_inspected_sample_size\": \"108\",\n"
    "    \"boxes_inspected\": null,\n"
    "    \"c\": null\n"
    "}\n"
    "```\n"
    "### **Here is the text for the ITEM:**\n"
)

def get_qc_prompt(text):
    prompt = f"""{REPORT_PROMPT}{text}"""
    return prompt

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
    "seed": 42,
}
