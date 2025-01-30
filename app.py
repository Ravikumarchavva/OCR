import streamlit as st
from pathlib import Path
import base64
import streamlit.components.v1 as components
import google.generativeai as genai
from main_logic import InvoiceExtractor

# Load API Key from Streamlit Secrets
GCP_KEY = st.secrets["GCP_KEY"]
genai.configure(api_key=GCP_KEY)

# Initialize the model
model = genai.GenerativeModel("gemini-2.0-flash-exp")
extractor = InvoiceExtractor(model)

# Set Streamlit page layout
st.set_page_config(layout="wide")
st.title("Invoice Extraction App")

# Custom CSS to increase content width
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

# Function to encode PDF in base64
def get_pdf_base64(pdf_path):
    """Encodes the PDF file in Base64 format for embedding."""
    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    return f"data:application/pdf;base64,{base64_pdf}"

# File uploader for PDF
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Save uploaded PDF to a temporary location
    temp_pdf_path = Path("temp_uploaded.pdf")
    with open(temp_pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Try extracting invoice details
    try:
        invoices = extractor.extract_all(temp_pdf_path.parent, limit=1)

        if invoices:
            invoice = invoices[0]

            # Display PDF and extracted data side by side
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Uploaded PDF")
                pdf_base64 = get_pdf_base64(temp_pdf_path)
                pdf_viewer_html = f"""
                <iframe src="{pdf_base64}" width="100%" height="600px"></iframe>
                """
                components.v1.html(pdf_viewer_html, height=600)

            with col2:
                st.subheader("Extracted Invoice Data")
                st.json(invoice.data)

        else:
            st.error("No invoices found in the uploaded PDF.")

    except Exception as e:
        st.error(f"An error occurred while extracting the invoice: {e}")
