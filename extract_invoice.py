import argparse
import os
from pathlib import Path
from datetime import datetime

from ocr_to_word_excel_fixed import process_invoice

EXTRACTED_DIR = Path('extracted_data')


def find_latest_outputs() -> tuple[str | None, str | None]:
    if not EXTRACTED_DIR.exists():
        return None, None
    excel = [p for p in EXTRACTED_DIR.iterdir() if p.suffix.lower() == '.xlsx']
    docx = [p for p in EXTRACTED_DIR.iterdir() if p.suffix.lower() == '.docx']
    latest_excel = str(max(excel, key=lambda p: p.stat().st_mtime)) if excel else None
    latest_docx = str(max(docx, key=lambda p: p.stat().st_mtime)) if docx else None
    return latest_excel, latest_docx


def main():
    parser = argparse.ArgumentParser(description='Extract invoice data to Excel/Word (no website needed).')
    parser.add_argument('--input', '-i', required=False, default='invoices/your_invoice.pdf',
                        help='Path to invoice file (pdf/png/jpg/jpeg). Default: invoices/your_invoice.pdf')
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ File not found: {input_path}")
        return 1

    print(f"➡️  Processing: {input_path}")
    success = process_invoice(str(input_path))
    if not success:
        print("❌ Extraction failed")
        return 2

    excel, docx = find_latest_outputs()
    print("✅ Extraction complete")
    if excel:
        print(f"📊 Excel: {excel}")
    if docx:
        print(f"📄 Word:  {docx}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

