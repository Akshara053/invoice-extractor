"""
Configuration file for Invoice Data Extractor
Customize patterns and settings here
"""

# OCR Model Settings
OCR_CONFIDENCE_THRESHOLD = 0.7
MAX_TEXT_LENGTH = 1000

# File Paths
DEFAULT_INPUT_FOLDER = "invoices"
DEFAULT_OUTPUT_FOLDER = "extracted_data"

# Custom Regex Patterns (add your specific patterns here)
CUSTOM_PATTERNS = {
    'invoice_number': [
        # Add your specific invoice number patterns
        r'invoice\s*#?\s*:?\s*([A-Z0-9\-_]+)',
        r'invoice\s*number\s*:?\s*([A-Z0-9\-_]+)',
        r'inv\s*:?\s*([A-Z0-9\-_]+)',
        r'#\s*([A-Z0-9\-_]+)',
        # Add more patterns as needed
    ],
    
    'date': [
        # Add your specific date patterns
        r'(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})',
        r'(\d{4}[/\-]\d{1,2}[/\-]\d{1,2})',
        r'(\d{1,2}\s+\w+\s+\d{4})',
        r'date\s*:?\s*(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})',
        # Add more patterns as needed
    ],
    
    'trn': [
        # Add your specific TRN patterns
        r'trn\s*:?\s*(\d{9,15})',
        r'tax\s*registration\s*number\s*:?\s*(\d{9,15})',
        r'vat\s*number\s*:?\s*(\d{9,15})',
        r'(\d{9,15})',
        # Add more patterns as needed
    ],
    
    'amount': [
        # Add your specific amount patterns
        r'total\s*:?\s*([\d,]+\.?\d*)\s*([A-Z]{3})',
        r'amount\s*:?\s*([\d,]+\.?\d*)\s*([A-Z]{3})',
        r'([\d,]+\.?\d*)\s*([A-Z]{3})',
        r'([\d,]+\.?\d*)',
        # Add more patterns as needed
    ],
    
    'vat_amount': [
        # Add your specific VAT patterns
        r'vat\s*:?\s*([\d,]+\.?\d*)',
        r'tax\s*:?\s*([\d,]+\.?\d*)',
        r'gst\s*:?\s*([\d,]+\.?\d*)',
        # Add more patterns as needed
    ],
    
    'quantity': [
        # Add your specific quantity patterns
        r'quantity\s*:?\s*([\d,]+\.?\d*)\s*m',
        r'qty\s*:?\s*([\d,]+\.?\d*)\s*m',
        r'([\d,]+\.?\d*)\s*meters',
        r'([\d,]+\.?\d*)\s*m',
        # Add more patterns as needed
    ]
}

# Company Name Detection Settings
COMPANY_NAME_MIN_LENGTH = 3
COMPANY_NAME_EXCLUDE_WORDS = [
    'INVOICE', 'DATE', 'TOTAL', 'AMOUNT', 'VAT', 'TRN', 'QUANTITY'
]

# Output Settings
EXCEL_SHEET_NAME = 'Invoice Data'
WORD_TITLE = 'Invoice Data Extraction Report'
WORD_TABLE_STYLE = 'Table Grid'

# Processing Settings
BATCH_SIZE = 10  # Process invoices in batches
SAVE_INTERMEDIATE = True  # Save progress after each batch 