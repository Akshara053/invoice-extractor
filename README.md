# Invoice Data Extractor

A comprehensive Python tool for extracting data from scanned PDF invoices using Doctr OCR. This tool automatically extracts key invoice fields and saves the data to both Excel and Word formats.

## ✅ Features

- **OCR Processing**: Uses Doctr OCR for accurate text extraction from scanned PDFs
- **Comprehensive Field Extraction**:
  - Company Name (using uppercase heuristic)
  - Invoice Number
  - Date (multiple formats supported)
  - Seller & Buyer TRN (Tax Registration Number)
  - Total Quantity (in meters)
  - Total Amount with Currency
  - VAT Amount
- **Multiple Output Formats**: Saves data to both Excel (.xlsx) and Word (.docx)
- **Batch Processing**: Process multiple invoices at once
- **Customizable Patterns**: Easy to add custom regex patterns for specific invoice formats
- **Error Handling**: Robust error handling and progress tracking

## 📋 Requirements

- Python 3.7+
- Windows 10/11 (tested on Windows 10.0.26100)

## 🚀 Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create necessary folders**:
   ```bash
   mkdir invoices
   mkdir extracted_data
   ```

## 📁 Project Structure

```
invoice/
├── invoice_extractor.py      # Main extraction script
├── config.py                 # Configuration and patterns
├── example_usage.py          # Usage examples
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── invoices/                 # Put your PDF invoices here
└── extracted_data/           # Output files will be saved here
```

## 🎯 Usage

### Basic Usage

1. **Place your PDF invoices** in the `invoices` folder

2. **Run the extractor**:
   ```bash
   python invoice_extractor.py
   ```

3. **Check results** in the `extracted_data` folder:
   - Excel file: `invoice_data_YYYYMMDD_HHMMSS.xlsx`
   - Word file: `invoice_report_YYYYMMDD_HHMMSS.docx`

### Advanced Usage

#### Single Invoice Processing
```python
from invoice_extractor import InvoiceDataExtractor

# Initialize extractor
extractor = InvoiceDataExtractor()

# Extract data from single invoice
data = extractor.extract_invoice_data("invoices/my_invoice.pdf")
print(data)
```

#### Batch Processing
```python
# Process all invoices in a folder
extractor.process_invoices("invoices", "output")
```

#### Custom Patterns
```python
# Add custom patterns for your specific invoice format
custom_patterns = {
    'invoice_number': [
        r'bill\s*#\s*([A-Z0-9\-_]+)',
        r'order\s*([A-Z0-9\-_]+)'
    ]
}
extractor.patterns.update(custom_patterns)
```

## 🔧 Configuration

Edit `config.py` to customize:

- **OCR Settings**: Confidence thresholds, text length limits
- **Patterns**: Add custom regex patterns for your invoice formats
- **Output Settings**: Excel sheet names, Word document styling
- **Processing Settings**: Batch sizes, intermediate saves

## 📊 Extracted Fields

| Field | Description | Example |
|-------|-------------|---------|
| Company Name | Extracted using uppercase heuristic | "ABC COMPANY LTD" |
| Invoice Number | Various formats supported | "INV-001", "12345" |
| Date | Multiple date formats | "2024-01-15", "15/01/2024" |
| Seller TRN | Tax Registration Number | "123456789" |
| Buyer TRN | Tax Registration Number | "987654321" |
| Total Quantity | In meters | "100.5" |
| Total Amount | With currency | "1500.00 USD" |
| VAT Amount | Tax amount | "150.00" |

## 🛠️ Customization

### Adding Custom Patterns

1. **Edit `config.py`**:
   ```python
   CUSTOM_PATTERNS = {
       'invoice_number': [
           # Add your patterns here
           r'your\s*pattern\s*([A-Z0-9\-_]+)'
       ]
   }
   ```

2. **Update the main script** to use custom patterns:
   ```python
   from config import CUSTOM_PATTERNS
   extractor.patterns.update(CUSTOM_PATTERNS)
   ```

### Supporting New Invoice Formats

1. **Analyze your invoice format**
2. **Create regex patterns** for each field
3. **Add patterns** to the configuration
4. **Test with sample invoices**

## 📝 Example Output

### Excel Format
- Organized table with all extracted fields
- Auto-adjusted column widths
- Timestamped filename

### Word Format
- Professional report layout
- Summary statistics
- Formatted table with headers

## ⚠️ Troubleshooting

### Common Issues

1. **"No PDF files found"**
   - Ensure PDF files are in the `invoices` folder
   - Check file extensions are `.pdf` (lowercase)

2. **"No text extracted"**
   - PDF might be image-based (scanned)
   - Ensure PDF is not password-protected
   - Check PDF quality (higher resolution = better OCR)

3. **"Pattern not found"**
   - Add custom patterns in `config.py`
   - Check invoice format matches existing patterns

4. **Installation errors**
   - Update pip: `python -m pip install --upgrade pip`
   - Install Visual C++ build tools (Windows)
   - Use virtual environment

### Performance Tips

- **Batch processing**: Process multiple invoices together
- **Image quality**: Use high-resolution scans for better OCR
- **Pattern optimization**: Refine regex patterns for your specific format

## 🔄 Updates and Maintenance

- **Regular updates**: Keep dependencies updated
- **Pattern refinement**: Improve patterns based on new invoice formats
- **Error logging**: Monitor extraction success rates

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review example usage in `example_usage.py`
3. Customize patterns in `config.py`

## 📄 License

This project is provided as-is for educational and commercial use.

---

**Happy Invoice Processing! 🎉** 