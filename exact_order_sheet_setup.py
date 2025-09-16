#!/usr/bin/env python3
"""
Exact Order Google Sheet Setup

This script sets up the Google Sheet with headers in the EXACT same order as the ERP report.
"""

import gspread
from google.oauth2.service_account import Credentials

# Scopes for the Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Path to your credentials file
CREDS_FILE = '/home/ubuntu/service_account.json'

# The ID of the spreadsheet
SPREADSHEET_ID = '1F8qZA-b9oMtqw2Mf0ybb6FE2tUgmKEZ3zjAN9jfg4Ag'

def get_gspread_client():
    """Get an authenticated gspread client."""
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client

def setup_exact_order_headers(client):
    """Sets up headers in the EXACT same order as the ERP report."""
    try:
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        worksheet = spreadsheet.get_worksheet(0) # Get the first sheet
        
        # Clear existing content
        worksheet.clear()
        
        # Headers in EXACT order as they appear in the ERP filter checkboxes (reading left to right, top to bottom)
        exact_order_headers = [
            # Row 1 - Top row of filter checkboxes
            "#",                    # Table row number
            "Hub",                  # Hub
            "Client Name",          # Client Name  
            "Nationality",          # Nationality
            "Email",                # Email
            "Operator",             # Operator
            
            # Row 2 - Second row of filter checkboxes
            "File Status",          # File Status
            "Arrival",              # Arrival
            "Departure",            # Departure  
            "Pax",                  # Pax
            "Lead / Operation",     # Lead / Operati
            
            # Row 3 - Third row of filter checkboxes
            "Request Channel",      # Request Channel
            "Communication",        # Communication
            "Medium",               # Medium
            "Offered Income",       # Offered Income
            "Offered Income (USD)", # Offered Incom (appears to be USD version)
            
            # Row 4 - Fourth row of filter checkboxes
            "Actual Paid Amount",       # Actual Paid Amount
            "Actual Paid Amount (USD)", # Actual Paid Amount (USD)
            "Remaining Payment",        # Remaining Payment
            "Remaining Payment (USD)",  # Remaining Payment (USD)
            "Submission Date",          # Submission Da
            
            # Row 5 - Fifth row of filter checkboxes
            "Confirmation Date",    # Confirmation Date
            "Company",              # Company
            "Department",           # Department
            "Product Title",        # Product Title
            "UTM Campaign",         # Utm Campaig
            
            # Row 6 - Sixth row of filter checkboxes
            "Initial Price",        # Initial Price
            "Device Type",          # Device Type
            
            # Additional fields from individual lead pages (not in filter but in ERP)
            "Client Phone",         # From table display
            "File No",              # File number
            "Request Token",        # Request Token
            "Sales Person",         # Sales Person
            "Request Status",       # Request Status
            "Source",               # Source
            "VIP Status",           # VIP Status
            "Loyalty Program",      # Loyalty Program
            "Group",                # Group booking
            "Has Int. Flight",      # International flight
            "Single Room",          # Room types
            "Double Room",
            "Triple Room", 
            "Family Room",
            "Int.Flight Amount",    # Flight amount
            "Int.Flight Currency",  # Flight currency
            "Agent / Group Discount", # Discounts
            
            # Custom enrichment columns (added at the end)
            "Agent Score",          # Sales agent performance score
            "Agent Recommendation", # Performance recommendation
            "IP Country",           # Geolocation country
            "IP State/Region",      # Geolocation state/region
            "IP City",              # Geolocation city
            "Profitability Flag",   # Business intelligence flag
            "Communication Count",  # Number of communications
            "Last Updated",         # Sync timestamp
            "Lead ID",              # Internal lead ID
            "Lead URL"              # Direct link to lead
        ]

        # Insert headers in the first row
        worksheet.insert_row(exact_order_headers, 1)
        
        # Format the header row
        worksheet.format('1:1', {
            'textFormat': {'bold': True},
            'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
        })
        
        print(f"✅ Headers set in EXACT ERP order ({len(exact_order_headers)} columns)")
        print("📋 Header order matches ERP filter layout:")
        
        # Show the order in groups
        print("\n🔹 Basic Info (Table Display):")
        for i in range(6):
            print(f"   {i+1:2d}. {exact_order_headers[i]}")
            
        print("\n🔹 ERP Filter Row 2:")
        for i in range(6, 11):
            print(f"   {i+1:2d}. {exact_order_headers[i]}")
            
        print("\n🔹 ERP Filter Row 3:")
        for i in range(11, 16):
            print(f"   {i+1:2d}. {exact_order_headers[i]}")
            
        print("\n🔹 ERP Filter Row 4:")
        for i in range(16, 21):
            print(f"   {i+1:2d}. {exact_order_headers[i]}")
            
        print("\n🔹 ERP Filter Row 5:")
        for i in range(21, 26):
            print(f"   {i+1:2d}. {exact_order_headers[i]}")
            
        print("\n🔹 ERP Filter Row 6:")
        for i in range(26, 28):
            print(f"   {i+1:2d}. {exact_order_headers[i]}")
            
        print("\n🔹 Additional ERP Fields:")
        for i in range(28, 42):
            print(f"   {i+1:2d}. {exact_order_headers[i]}")
            
        print("\n🔹 Custom Enrichment:")
        for i in range(42, len(exact_order_headers)):
            print(f"   {i+1:2d}. {exact_order_headers[i]}")

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"❌ Spreadsheet with ID '{SPREADSHEET_ID}' not found.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    print("Setting up Google Sheet with EXACT ERP header order...")
    gspread_client = get_gspread_client()
    if gspread_client:
        setup_exact_order_headers(gspread_client)
        print(f"\n🔗 Google Sheet URL: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
        print("\n✅ Headers now match the exact order from your ERP report!")
