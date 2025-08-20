import pandas as pd
import os

# Find the most recent Excel file
excel_files = [f for f in os.listdir('extracted_data') if f.endswith('.xlsx')]
if excel_files:
    latest_file = max(excel_files, key=lambda x: os.path.getctime(os.path.join('extracted_data', x)))
    file_path = os.path.join('extracted_data', latest_file)
    
    print(f"Reading data from: {file_path}")
    print("=" * 80)
    
    # Read the Excel file
    df = pd.read_excel(file_path)
    
    # Display the data
    print("Extracted Invoice Data with VAT Amounts:")
    print(df.to_string(index=False))
    
    print("\n" + "=" * 80)
    print(f"Total pages processed: {len(df)}")
    print(f"Columns extracted: {list(df.columns)}")
    
    # Show VAT amounts summary
    print("\nVAT Amounts Summary:")
    vat_col = 'VAT Amount' if 'VAT Amount' in df.columns else None
    if vat_col:
        vat_data = df[vat_col].dropna()
        print(f"Pages with VAT amounts: {len(vat_data)}")
        print("VAT amounts found:")
        for idx, vat in vat_data.items():
            page = df.loc[idx, 'Page']
            company = df.loc[idx, 'Company Name']
            print(f"  Page {page} ({company}): {vat}")
    
else:
    print("No Excel files found in extracted_data folder") 