import base64

class DataIngestion:
    def __init__(self):
        pass

    def transform(self, file_path):
        with open(file_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()
        return base64.standard_b64encode(pdf_data).decode("utf-8")