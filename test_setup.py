"""
Test script to verify the invoice extractor setup
Run this to check if all dependencies are installed correctly
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")
    
    try:
        import re
        print("✓ re module")
    except ImportError as e:
        print(f"✗ re module: {e}")
        return False
    
    try:
        import cv2
        print("✓ opencv-python")
    except ImportError as e:
        print(f"✗ opencv-python: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ numpy")
    except ImportError as e:
        print(f"✗ numpy: {e}")
        return False
    
    try:
        import pandas as pd
        print("✓ pandas")
    except ImportError as e:
        print(f"✗ pandas: {e}")
        return False
    
    try:
        from datetime import datetime
        print("✓ datetime")
    except ImportError as e:
        print(f"✗ datetime: {e}")
        return False
    
    try:
        from doctr.io import DocumentFile
        from doctr.models import ocr_predictor
        print("✓ doctr")
    except ImportError as e:
        print(f"✗ doctr: {e}")
        return False
    
    try:
        from docx import Document
        print("✓ python-docx")
    except ImportError as e:
        print(f"✗ python-docx: {e}")
        return False
    
    try:
        import openpyxl
        print("✓ openpyxl")
    except ImportError as e:
        print(f"✗ openpyxl: {e}")
        return False
    
    try:
        from PIL import Image
        print("✓ Pillow")
    except ImportError as e:
        print(f"✗ Pillow: {e}")
        return False
    
    return True

def test_folders():
    """Test if required folders exist"""
    print("\nTesting folders...")
    
    folders = ['invoices', 'extracted_data']
    for folder in folders:
        if os.path.exists(folder):
            print(f"✓ {folder} folder exists")
        else:
            print(f"✗ {folder} folder missing")
            return False
    
    return True

def test_files():
    """Test if required files exist"""
    print("\nTesting files...")
    
    files = [
        'invoice_extractor.py',
        'config.py',
        'example_usage.py',
        'requirements.txt',
        'README.md'
    ]
    
    for file in files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} missing")
            return False
    
    return True

def test_ocr_model():
    """Test if OCR model can be loaded"""
    print("\nTesting OCR model...")
    
    try:
        from doctr.models import ocr_predictor
        model = ocr_predictor(pretrained=True)
        print("✓ OCR model loaded successfully")
        return True
    except Exception as e:
        print(f"✗ OCR model failed to load: {e}")
        return False

def main():
    """Run all tests"""
    print("Invoice Data Extractor - Setup Test")
    print("=" * 40)
    
    # Test Python version
    print(f"Python version: {sys.version}")
    
    # Run tests
    tests = [
        test_imports,
        test_folders,
        test_files,
        test_ocr_model
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! Setup is complete.")
        print("\nNext steps:")
        print("1. Place your PDF invoices in the 'invoices' folder")
        print("2. Run: python invoice_extractor.py")
        print("3. Check results in the 'extracted_data' folder")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Create missing folders: mkdir invoices extracted_data")
        print("3. Check file permissions and paths")

if __name__ == "__main__":
    main() 