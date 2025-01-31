from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path

from components.data_ingestion import DataIngestion
from components.model import OCR_Model

data_ingestion = DataIngestion()
ocr_model = OCR_Model(model="gemini-2.0-flash-exp")

app = FastAPI()

@app.post("/extract-invoice/")
async def extract_invoice(filename: UploadFile = File(...)):
    if filename.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, 
            detail="Invalid file format. Only PDF files are accepted."
        )
    try:
        # Save the uploaded PDF to a temporary location
        temp_pdf_path = Path("temp_uploaded.pdf")
        with open(temp_pdf_path, "wb") as f:
            f.write(await filename.read())
        
        # Convert the uploaded PDF to base64 using DataIngestion
        pdf_data = data_ingestion.transform(temp_pdf_path)
        
        # Extract invoice data
        invoice = ocr_model.extract(pdf_data)
        invoice_data = invoice.data
        line_items = invoice_data.pop("line_items", [])
        headers = invoice_data
        headers["filename"] = filename.filename
        return JSONResponse(content={
            "data": {
                "lineitems": line_items,
                "headers": headers
            }
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while extracting the invoice: {e}")
    
# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
