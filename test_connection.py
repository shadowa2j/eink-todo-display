#!/usr/bin/env python3
"""
Test script to verify Google Sheets connection
Run this before trying the full display to make sure credentials work
"""

import sys
import os
from datetime import datetime

try:
    import gspread
    from google.oauth2.service_account import Credentials
except ImportError:
    print("ERROR: Required Python packages not installed!")
    print("Please run: pip3 install -r requirements.txt --break-system-packages")
    sys.exit(1)

def test_google_sheets():
    """Test Google Sheets connection"""
    
    CREDENTIALS_FILE = 'credentials.json'
    SHEET_NAME = 'My To-Do List'  # Change this to match your sheet name
    
    print("=" * 50)
    print("Google Sheets Connection Test")
    print("=" * 50)
    print()
    
    # Check credentials file
    print("1. Checking for credentials file...")
    if not os.path.exists(CREDENTIALS_FILE):
        print("   ❌ FAILED: credentials.json not found!")
        print()
        print("   Please:")
        print("   - Follow SETUP_INSTRUCTIONS.md to create credentials")
        print("   - Copy credentials.json to this folder")
        return False
    print("   ✓ Found credentials.json")
    print()
    
    # Try to authenticate
    print("2. Authenticating with Google...")
    try:
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scope)
        client = gspread.authorize(creds)
        print("   ✓ Authentication successful")
        print()
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        print()
        print("   Check that your credentials.json file is valid")
        return False
    
    # Try to open the sheet
    print(f"3. Opening sheet '{SHEET_NAME}'...")
    try:
        sheet = client.open(SHEET_NAME).sheet1
        print("   ✓ Sheet found and opened")
        print()
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        print()
        print("   Possible issues:")
        print("   - Sheet name doesn't match (check spelling and capitalization)")
        print("   - Sheet not shared with service account")
        print()
        print("   Service account email (from credentials.json):")
        try:
            import json
            with open(CREDENTIALS_FILE) as f:
                data = json.load(f)
                print(f"   {data.get('client_email', 'NOT FOUND')}")
                print()
                print("   Make sure to share your Google Sheet with this email!")
        except:
            pass
        return False
    
    # Try to read data
    print("4. Reading data from sheet...")
    try:
        records = sheet.get_all_records()
        print(f"   ✓ Found {len(records)} rows")
        print()
        
        if len(records) == 0:
            print("   ⚠ WARNING: Sheet is empty!")
            print("   Add some tasks to test properly")
        else:
            print("   Sample tasks:")
            for i, record in enumerate(records[:3]):
                task = record.get('Task', 'NO TASK COLUMN')
                status = record.get('Status', 'NO STATUS COLUMN')
                print(f"   - {task} [{status if status else 'active'}]")
            if len(records) > 3:
                print(f"   ... and {len(records) - 3} more")
        print()
        
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        print()
        print("   Make sure your sheet has columns named 'Task' and 'Status'")
        return False
    
    # Success!
    print("=" * 50)
    print("✓ ALL TESTS PASSED!")
    print("=" * 50)
    print()
    print("Your Google Sheets connection is working correctly!")
    print("You can now run: python3 todo_display.py")
    print()
    return True

if __name__ == "__main__":
    success = test_google_sheets()
    sys.exit(0 if success else 1)
