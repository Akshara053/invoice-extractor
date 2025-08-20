"""
Example usage of the Invoice Data Extractor
This script demonstrates different ways to use the extractor
"""

from invoice_extractor import InvoiceDataExtractor
import os

def example_single_invoice():
    """
    Example: Extract data from a single invoice
    """
    print("=== Single Invoice Extraction Example ===")
    
    # Initialize extractor
    extractor = InvoiceDataExtractor()
    
    # Path to your single invoice
    pdf_path = "invoices/sample_invoice.pdf"
    
    if os.path.exists(pdf_path):
        # Extract data
        data = extractor.extract_invoice_data(pdf_path)
        
        # Print results
        print("\nExtracted Data:")
        for key, value in data.items():
            print(f"{key}: {value}")
    else:
        print(f"File not found: {pdf_path}")
        print("Please place a PDF invoice in the 'invoices' folder")

def example_batch_processing():
    """
    Example: Process multiple invoices in batch
    """
    print("\n=== Batch Processing Example ===")
    
    # Initialize extractor
    extractor = InvoiceDataExtractor()
    
    # Process all invoices in the folder
    input_folder = "invoices"
    output_folder = "extracted_data"
    
    if os.path.exists(input_folder):
        extractor.process_invoices(input_folder, output_folder)
    else:
        print(f"Folder not found: {input_folder}")
        print("Please create an 'invoices' folder and add PDF files")

def example_custom_extraction():
    """
    Example: Custom extraction with specific patterns
    """
    print("\n=== Custom Extraction Example ===")
    
    # Initialize extractor
    extractor = InvoiceDataExtractor()
    
    # Add custom patterns for your specific invoice format
    custom_patterns = {
        'invoice_number': [
            r'bill\s*#\s*([A-Z0-9\-_]+)',
            r'order\s*([A-Z0-9\-_]+)'
        ],
        'amount': [
            r'grand\s*total\s*:?\s*([\d,]+\.?\d*)\s*([A-Z]{3})',
            r'final\s*amount\s*:?\s*([\d,]+\.?\d*)\s*([A-Z]{3})'
        ]
    }
    
    # Update patterns
    extractor.patterns.update(custom_patterns)
    
    # Process with custom patterns
    pdf_path = "invoices/custom_invoice.pdf"
    if os.path.exists(pdf_path):
        data = extractor.extract_invoice_data(pdf_path)
        print("Custom extraction results:")
        for key, value in data.items():
            print(f"{key}: {value}")

def example_save_formats():
    """
    Example: Save data in different formats
    """
    print("\n=== Save Formats Example ===")
    
    # Initialize extractor
    extractor = InvoiceDataExtractor()
    
    # Sample data (you would normally extract this)
    sample_data = [
        {
            'file_name': 'invoice1.pdf',
            'company_name': 'ABC COMPANY LTD',
            'invoice_number': 'INV-001',
            'date': '2024-01-15',
            'seller_trn': '123456789',
            'buyer_trn': '987654321',
            'total_quantity_meters': '100.5',
            'total_amount': '1500.00 USD',
            'vat_amount': '150.00',
            'extraction_date': '2024-01-15 10:30:00'
        },
        {
            'file_name': 'invoice2.pdf',
            'company_name': 'XYZ CORPORATION',
            'invoice_number': 'INV-002',
            'date': '2024-01-16',
            'seller_trn': '111222333',
            'buyer_trn': '444555666',
            'total_quantity_meters': '75.2',
            'total_amount': '1128.00 USD',
            'vat_amount': '112.80',
            'extraction_date': '2024-01-15 10:30:00'
        }
    ]
    
    # Save to Excel
    excel_path = "extracted_data/sample_data.xlsx"
    extractor.save_to_excel(sample_data, excel_path)
    
    # Save to Word
    word_path = "extracted_data/sample_report.docx"
    extractor.save_to_word(sample_data, word_path)
    
    print("Sample data saved to Excel and Word formats")

def main():
    """
    Run all examples
    """
    print("Invoice Data Extractor - Example Usage")
    print("=" * 50)
    
    # Create necessary folders
    os.makedirs("invoices", exist_ok=True)
    os.makedirs("extracted_data", exist_ok=True)
    
    # Run examples
    example_single_invoice()
    example_batch_processing()
    example_custom_extraction()
    example_save_formats()
    
    print("\n" + "=" * 50)
    print("Examples completed!")
    print("\nTo use the extractor:")
    print("1. Place your PDF invoices in the 'invoices' folder")
    print("2. Run: python invoice_extractor.py")
    print("3. Check the 'extracted_data' folder for results")

if __name__ == "__main__":
    main() 