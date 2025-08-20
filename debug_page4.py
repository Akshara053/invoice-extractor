import os
os.environ["USE_TORCH"] = "1"
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import re

PDF_PATH = "invoices/your_invoice.pdf"
model = ocr_predictor(pretrained=True)
doc = DocumentFile.from_pdf(PDF_PATH)
result = model(doc)

# Get page 4 (index 3)
page_idx = 3
page = result.pages[page_idx]
page_lines = []

for block in page.blocks:
    for line in block.lines:
        line_text = " ".join([word.value for word in line.words])
        page_lines.append(line_text)

print(f"=== ALL OCR LINES FOR PAGE 4 ===")
for i, line in enumerate(page_lines):
    print(f"{i+1}: {line}")

print(f"\n=== SEARCHING FOR AED AMOUNTS ===")
for i, line in enumerate(page_lines):
    if 'AED' in line:
        print(f"Line {i+1}: {line}")
        # Find all AED amounts in this line
        matches = re.findall(r'AED\s*[\d,.]+', line)
        for match in matches:
            print(f"  Found: {match}")

print(f"\n=== SEARCHING FOR TOTAL LINES ===")
for i, line in enumerate(page_lines):
    if 'TOTAL' in line.upper():
        print(f"Line {i+1}: {line}")
        # Check next 3 lines for AED amounts
        for j in range(i, min(i+4, len(page_lines))):
            if j != i:  # Skip the current line
                next_line = page_lines[j]
                if 'AED' in next_line:
                    print(f"  Next line {j+1}: {next_line}")
                    matches = re.findall(r'AED\s*[\d,.]+', next_line)
                    for match in matches:
                        print(f"    Found: {match}") 