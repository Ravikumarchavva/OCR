import base64

class DataIngestion:
    def __init__(self):
        pass

    def transform(self, file_path):
        '''Reads a PDF file and returns its base64 encoded content.'''
        with open(file_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()
        return base64.standard_b64encode(pdf_data).decode("utf-8")