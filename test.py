import pdfplumber

pdf_path = "uploads/haritha.pdf"

with pdfplumber.open(pdf_path) as pdf:

    for page in pdf.pages:

        text = page.extract_text()

        print(text)