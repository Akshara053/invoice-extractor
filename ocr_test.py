import os
os.environ["USE_TORCH"] = "1"
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

PDF_PATH = "invoices/your_invoice.pdf"

model = ocr_predictor(pretrained=True)
doc = DocumentFile.from_pdf(PDF_PATH)
result = model(doc)

print("\n--- OCR RAW OUTPUT ---\n")
for page_idx, page in enumerate(result.pages):
    print(f"Page {page_idx+1}:")
    for block in page.blocks:
        for line in block.lines:
            line_text = " ".join([word.value for word in line.words])
            print(line_text)
    print("\n--- End of Page ---\n") 