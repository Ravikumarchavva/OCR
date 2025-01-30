from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
from main_logic import InvoiceExtractor
import google.generativeai as genai

import os
from dotenv import load_dotenv
load_dotenv()

GCP_KEY = os.getenv("GCP_KEY")

genai.configure(api_key=GCP_KEY)
model = genai.GenerativeModel("gemini-2.0-flash-exp")

extractor = InvoiceExtractor(model)

app = FastAPI()

@app.post("/extract-invoice/")
async def extract_invoice(file: UploadFile = File(...)):
    try:
        # Save the uploaded PDF to a temporary location
        temp_pdf_path = Path("temp_uploaded.pdf")
        with open(temp_pdf_path, "wb") as f:
            f.write(await file.read())
        
        # Extract invoice data
        invoices = extractor.extract_all(temp_pdf_path.parent, limit=1)
        if invoices:
            invoice = invoices[0]
            return JSONResponse(content={"data": invoice.data})
        else:
            raise HTTPException(status_code=404, detail="No invoices found in the uploaded PDF.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while extracting the invoice: {e}")
    
# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
