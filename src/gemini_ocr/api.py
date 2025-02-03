from fastapi import FastAPI, File, UploadFile, HTTPException, Response
from fastapi.responses import JSONResponse
from pathlib import Path

from components.data_ingestion import DataIngestion
from components.model import OCR_Model

from config.configs import MODEL

app = FastAPI()

@app.post("/extract-invoice/")
async def extract_invoice(filename: UploadFile = File(...)):

    # Check the file type
    if not (filename.filename.endswith(".pdf") or filename.filename.endswith(".tiff")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and TIFF files are allowed.")
    
    print(filename)
    try:
        # Save the uploaded file to a temporary location
        temp_file_path = Path(f"temp_uploaded{Path(filename.filename).suffix}")
        with open(temp_file_path, "wb") as f:
            f.write(await filename.read())
        
        # Initialize DataIngestion and OCR_Model
        data_ingestion = DataIngestion()
        ocr_model = OCR_Model(model=MODEL)

        # Convert the uploaded file to base64 using DataIngestion
        pdf_data = data_ingestion.transform(temp_file_path)
        
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
