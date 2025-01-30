import streamlit as st
from pathlib import Path
from main_logic import InvoiceExtractor
import base64

import google.generativeai as genai

GCP_KEY = st.secrets["GCP_KEY"]

genai.configure(api_key=GCP_KEY)
model = genai.GenerativeModel("gemini-2.0-flash-exp")

extractor = InvoiceExtractor(model)

st.set_page_config(layout="wide")

st.title("Invoice Extraction App")

# Add custom CSS for 90% width
st.markdown(
    """
    <style>
    .reportview-container .main .block-container {
        max-width: 90%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Save the uploaded PDF to a temporary location
    temp_pdf_path = Path("temp_uploaded.pdf")
    with open(temp_pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Display the PDF using an iframe
    st.markdown(
        f'<iframe src="temp_uploaded.pdf" width="100%" height="600px" type="application/pdf"></iframe>',
        unsafe_allow_html=True,
    )
    
    # Extract invoices
    try:
        invoices = extractor.extract_all(temp_pdf_path.parent, limit=1)
        if invoices:
            invoice = invoices[0]
            
            # Display PDF and extracted data side by side
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Uploaded PDF")
            
            with col2:
                st.subheader("Extracted Invoice Data")
                st.json(invoice.data)
        else:
            st.error("No invoices found in the uploaded PDF.")
    except Exception as e:
        st.error(f"An error occurred while extracting the invoice: {e}")