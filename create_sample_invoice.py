"""
Create a sample invoice PDF for testing the extraction system
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import os

def create_sample_invoice():
    """Create a sample invoice PDF for testing"""
    
    # Create the PDF document
    doc = SimpleDocTemplate("invoices/sample_invoice.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    company_style = ParagraphStyle(
        'CompanyName',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=20,
        alignment=0  # Left alignment
    )
    
    # Story to hold all elements
    story = []
    
    # Add title
    story.append(Paragraph("INVOICE", title_style))
    story.append(Spacer(1, 20))
    
    # Add company information
    story.append(Paragraph("ABC COMPANY LTD", company_style))
    story.append(Paragraph("123 Business Street", styles['Normal']))
    story.append(Paragraph("City, State 12345", styles['Normal']))
    story.append(Paragraph("Phone: (555) 123-4567", styles['Normal']))
    story.append(Paragraph("Email: info@abccompany.com", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Add invoice details
    invoice_data = [
        ['Invoice Number:', 'INV-2024-001'],
        ['Date:', '2024-01-15'],
        ['Due Date:', '2024-02-15'],
        ['TRN:', '123456789'],
    ]
    
    invoice_table = Table(invoice_data, colWidths=[2*inch, 3*inch])
    invoice_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(invoice_table)
    story.append(Spacer(1, 20))
    
    # Add customer information
    story.append(Paragraph("Bill To:", styles['Heading3']))
    story.append(Paragraph("XYZ CORPORATION", styles['Normal']))
    story.append(Paragraph("456 Customer Avenue", styles['Normal']))
    story.append(Paragraph("Customer City, CS 67890", styles['Normal']))
    story.append(Paragraph("TRN: 987654321", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Add items table
    story.append(Paragraph("Items:", styles['Heading3']))
    
    items_data = [
        ['Description', 'Quantity (m)', 'Unit Price', 'Amount'],
        ['Premium Fabric Material', '100.5', '$15.00', '$1,507.50'],
        ['Shipping & Handling', '1', '$50.00', '$50.00'],
    ]
    
    items_table = Table(items_data, colWidths=[2.5*inch, 1*inch, 1*inch, 1*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    story.append(items_table)
    story.append(Spacer(1, 20))
    
    # Add totals
    totals_data = [
        ['Subtotal:', '$1,557.50'],
        ['VAT (10%):', '$155.75'],
        ['Total:', '$1,713.25 USD'],
    ]
    
    totals_table = Table(totals_data, colWidths=[4*inch, 1.5*inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (0, -1), (1, -1), 2, colors.black),
    ]))
    
    story.append(totals_table)
    story.append(Spacer(1, 30))
    
    # Add payment terms
    story.append(Paragraph("Payment Terms:", styles['Heading4']))
    story.append(Paragraph("Net 30 days. Please include invoice number with payment.", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Add thank you message
    story.append(Paragraph("Thank you for your business!", styles['Normal']))
    
    # Build the PDF
    doc.build(story)
    print("Sample invoice created: invoices/sample_invoice.pdf")

def create_second_sample():
    """Create a second sample invoice with different format"""
    
    doc = SimpleDocTemplate("invoices/sample_invoice_2.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    
    story = []
    
    # Add title
    story.append(Paragraph("BILL", styles['Heading1']))
    story.append(Spacer(1, 20))
    
    # Add company information
    story.append(Paragraph("TEXTILE SUPPLIERS INC", styles['Heading2']))
    story.append(Paragraph("789 Industrial Blvd", styles['Normal']))
    story.append(Paragraph("Manufacturing District, MD 54321", styles['Normal']))
    story.append(Paragraph("TRN: 111222333", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Add invoice details
    invoice_data = [
        ['Bill #:', 'BILL-2024-002'],
        ['Order Date:', '16/01/2024'],
        ['Delivery Date:', '20/01/2024'],
    ]
    
    invoice_table = Table(invoice_data, colWidths=[2*inch, 3*inch])
    invoice_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    
    story.append(invoice_table)
    story.append(Spacer(1, 20))
    
    # Add customer information
    story.append(Paragraph("Customer:", styles['Heading3']))
    story.append(Paragraph("FASHION RETAILERS LLC", styles['Normal']))
    story.append(Paragraph("321 Retail Street", styles['Normal']))
    story.append(Paragraph("Shopping Center, SC 13579", styles['Normal']))
    story.append(Paragraph("TRN: 444555666", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Add items
    story.append(Paragraph("Order Details:", styles['Heading3']))
    
    items_data = [
        ['Item', 'Qty (m)', 'Price', 'Total'],
        ['Cotton Fabric', '75.2', '$12.00', '$902.40'],
        ['Silk Material', '25.0', '$25.00', '$625.00'],
        ['Processing Fee', '1', '$100.00', '$100.00'],
    ]
    
    items_table = Table(items_data, colWidths=[2.5*inch, 1*inch, 1*inch, 1*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    story.append(items_table)
    story.append(Spacer(1, 20))
    
    # Add totals
    totals_data = [
        ['Subtotal:', '$1,627.40'],
        ['GST (5%):', '$81.37'],
        ['Grand Total:', '$1,708.77 USD'],
    ]
    
    totals_table = Table(totals_data, colWidths=[4*inch, 1.5*inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
        ('LINEBELOW', (0, -1), (1, -1), 2, colors.black),
    ]))
    
    story.append(totals_table)
    
    # Build the PDF
    doc.build(story)
    print("Second sample invoice created: invoices/sample_invoice_2.pdf")

def main():
    """Create sample invoices for testing"""
    print("Creating sample invoices for testing...")
    
    # Ensure invoices folder exists
    os.makedirs("invoices", exist_ok=True)
    
    # Create sample invoices
    create_sample_invoice()
    create_second_sample()
    
    print("\nSample invoices created successfully!")
    print("You can now test the extraction system by running:")
    print("python invoice_extractor.py")

if __name__ == "__main__":
    main() 