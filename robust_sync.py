#!/usr/bin/env python3
"""
Robust Memphis Tours ERP to Google Sheets Sync System

This script includes comprehensive error handling and logging for scheduled execution.
"""

import os
import sys
import time
import json
import requests
import gspread
import logging
import traceback
from datetime import datetime
from google.oauth2.service_account import Credentials

# Setup logging
log_file = '/home/ubuntu/sync_log.txt'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Configuration with absolute paths
SPREADSHEET_ID = '1F8qZA-b9oMtqw2Mf0ybb6FE2tUgmKEZ3zjAN9jfg4Ag'
SERVICE_ACCOUNT_FILE = '/home/ubuntu/service_account.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class RobustMemphisToursSync:
    def __init__(self):
        self.sheet = None
        logger.info("🚀 Initializing Memphis Tours Sync System...")
        
    def check_prerequisites(self):
        """Check if all required files and dependencies exist."""
        try:
            logger.info("🔍 Checking prerequisites...")
            
            # Check if service account file exists
            if not os.path.exists(SERVICE_ACCOUNT_FILE):
                logger.error(f"❌ Service account file not found: {SERVICE_ACCOUNT_FILE}")
                return False
            
            # Check if file is readable
            try:
                with open(SERVICE_ACCOUNT_FILE, 'r') as f:
                    json.load(f)
                logger.info("✅ Service account file is valid JSON")
            except Exception as e:
                logger.error(f"❌ Service account file is not valid JSON: {e}")
                return False
            
            # Check required Python packages
            required_packages = ['gspread', 'google', 'requests']
            for package in required_packages:
                try:
                    __import__(package)
                    logger.info(f"✅ Package {package} is available")
                except ImportError:
                    logger.error(f"❌ Package {package} is not installed")
                    return False
            
            # Check internet connectivity
            try:
                response = requests.get('https://www.google.com', timeout=10)
                if response.status_code == 200:
                    logger.info("✅ Internet connectivity confirmed")
                else:
                    logger.warning(f"⚠️ Unexpected response from Google: {response.status_code}")
            except Exception as e:
                logger.error(f"❌ No internet connectivity: {e}")
                return False
            
            logger.info("✅ All prerequisites check passed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error checking prerequisites: {e}")
            logger.error(traceback.format_exc())
            return False
    
    def setup_google_sheets(self):
        """Initialize Google Sheets connection with error handling."""
        try:
            logger.info("🔐 Setting up Google Sheets connection...")
            
            # Load credentials
            creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            logger.info("✅ Service account credentials loaded")
            
            # Authorize client
            client = gspread.authorize(creds)
            logger.info("✅ Google Sheets client authorized")
            
            # Open spreadsheet
            spreadsheet = client.open_by_key(SPREADSHEET_ID)
            logger.info(f"✅ Spreadsheet opened: {spreadsheet.title}")
            
            # Get worksheet
            self.sheet = spreadsheet.get_worksheet(0)
            logger.info(f"✅ Worksheet accessed: {self.sheet.title}")
            
            # Test write access
            try:
                # Try to read the first cell to test access
                test_value = self.sheet.cell(1, 1).value
                logger.info(f"✅ Sheet access confirmed. First cell: '{test_value}'")
            except Exception as e:
                logger.error(f"❌ Cannot access sheet data: {e}")
                return False
            
            logger.info("✅ Google Sheets connection established successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error setting up Google Sheets: {e}")
            logger.error(traceback.format_exc())
            return False
    
    def score_sales_agent(self, communications_count, lead_status):
        """Score sales agent performance based on available data."""
        try:
            score = 5  # Default score
            recommendation = "Standard performance"
            
            # Basic scoring algorithm
            if communications_count == 0:
                score = 3
                recommendation = "No response from agent yet"
            elif communications_count == 1:
                score = 6
                recommendation = "Initial contact made, needs follow-up"
            else:
                score = 8
                recommendation = "Active communication maintained"
            
            # Adjust score based on lead status
            status = str(lead_status).lower() if lead_status else ''
            if 'confirmed' in status:
                score = min(10, score + 2)
                recommendation = "Lead successfully converted"
            elif 'new' in status and communications_count > 0:
                score = max(1, score - 1)
                recommendation = "Response needed for new lead"
            
            return score, recommendation
            
        except Exception as e:
            logger.warning(f"⚠️ Error scoring agent: {e}")
            return 5, "Error calculating score"
    
    def get_ip_geolocation(self, ip_address):
        """Get geolocation data for an IP address with error handling."""
        if not ip_address or ip_address == "N/A":
            return {"country": "N/A", "region": "N/A", "city": "N/A"}
        
        try:
            logger.debug(f"🌍 Getting geolocation for IP: {ip_address}")
            response = requests.get(f"https://ipapi.co/{ip_address}/json/", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                result = {
                    "country": data.get("country_name", "N/A"),
                    "region": data.get("region", "N/A"),
                    "city": data.get("city", "N/A")
                }
                logger.debug(f"✅ Geolocation found: {result}")
                return result
            else:
                logger.warning(f"⚠️ Geolocation API returned status {response.status_code}")
                
        except Exception as e:
            logger.warning(f"⚠️ Error getting geolocation for {ip_address}: {e}")
        
        return {"country": "N/A", "region": "N/A", "city": "N/A"}
    
    def check_profitability(self, lead_data):
        """Check if lead has profitability issues."""
        try:
            flags = []
            
            # Check for solo traveler
            pax = str(lead_data.get('pax', '')).lower()
            if pax == '1' or 'solo' in pax:
                flags.append("Solo traveler (1 PAX)")
            
            # Check for shore excursion
            client_name = str(lead_data.get('client_name', '')).lower()
            if 'shore' in client_name or 'excursion' in client_name:
                flags.append("Shore excursion")
            
            # Check for low-value indicators
            if 'day trip' in client_name or 'half day' in client_name:
                flags.append("Short duration trip")
            
            result = "; ".join(flags) if flags else "No issues identified"
            logger.debug(f"💰 Profitability check: {result}")
            return result
            
        except Exception as e:
            logger.warning(f"⚠️ Error checking profitability: {e}")
            return "Error checking profitability"
    
    def add_sample_data_safe(self):
        """Add sample data with comprehensive error handling."""
        try:
            logger.info("📊 Adding sample lead data...")
            
            # Simple sample data for testing
            sample_leads = [
                {
                    'row_number': str(int(time.time()) % 1000),  # Unique row number
                    'hub': 'memphistours.com',
                    'client_name': f'Test Client {datetime.now().strftime("%H:%M")}',
                    'nationality': 'Test Country',
                    'email': 'test@example.com',
                    'operator': 'Memphis Tours',
                    'file_status': 'Active',
                    'arrival': '2025-10-15',
                    'departure': '2025-10-22',
                    'pax': '2',
                    'lead_operation': 'Lead',
                    'request_channel': 'Website',
                    'communication': 'Email',
                    'medium': 'Online',
                    'offered_income': '1000.00',
                    'offered_income_usd': '1000.00',
                    'actual_paid_amount': '0.00',
                    'actual_paid_amount_usd': '0.00',
                    'remaining_payment': '1000.00',
                    'remaining_payment_usd': '1000.00',
                    'submission_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'confirmation_date': 'N/A',
                    'company': 'Memphis Tours',
                    'department': 'Corporate Sales',
                    'product_title': 'Test Tour Package',
                    'utm_campaign': 'test_campaign',
                    'initial_price': '1000.00',
                    'device_type': 'Desktop',
                    'client_phone': '+1-555-0123',
                    'file_no': f'MT{int(time.time())}',
                    'request_token': f'TEST{int(time.time())}',
                    'sales_person': 'Test Agent',
                    'request_status': 'New Request',
                    'source': 'Test Site',
                    'vip_status': 'No',
                    'loyalty_program': 'Fresh Customer',
                    'group': 'No',
                    'has_int_flight': 'No',
                    'single_room': '0',
                    'double_room': '1',
                    'triple_room': '0',
                    'family_room': '0',
                    'int_flight_amount': '0',
                    'int_flight_currency': 'USD',
                    'agent_group_discount': '0',
                    'communications_count': 1,
                    'lead_id': f'TEST{int(time.time())}',
                    'lead_url': 'https://example.com/test'
                }
            ]
            
            # Process and enrich each lead
            enriched_leads = []
            for lead in sample_leads:
                logger.info(f"📝 Processing lead: {lead['client_name']}")
                
                # Score sales agent
                agent_score, agent_recommendation = self.score_sales_agent(
                    lead.get('communications_count', 0), 
                    lead.get('request_status', '')
                )
                
                # Add IP geolocation (using a test IP)
                geo_data = self.get_ip_geolocation('8.8.8.8')
                
                # Check profitability
                profitability_flag = self.check_profitability(lead)
                
                # Add enrichment data
                lead.update({
                    'agent_score': agent_score,
                    'agent_recommendation': agent_recommendation,
                    'ip_country': geo_data['country'],
                    'ip_region': geo_data['region'],
                    'ip_city': geo_data['city'],
                    'profitability_flag': profitability_flag,
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                
                enriched_leads.append(lead)
                logger.info(f"✅ Lead processed successfully")
            
            # Sync to Google Sheets
            synced_count = self.sync_to_google_sheets(enriched_leads)
            logger.info(f"✅ Sync completed! Added {synced_count} leads")
            return synced_count > 0
            
        except Exception as e:
            logger.error(f"❌ Error adding sample data: {e}")
            logger.error(traceback.format_exc())
            return False
    
    def sync_to_google_sheets(self, leads_data):
        """Sync data to Google Sheets with robust error handling."""
        try:
            logger.info("📤 Starting sync to Google Sheets...")
            
            if not self.sheet:
                logger.error("❌ No sheet connection available")
                return 0
            
            # Get existing data to avoid duplicates
            try:
                existing_data = self.sheet.get_all_records()
                existing_tokens = {row.get('Request Token', '') for row in existing_data}
                logger.info(f"📋 Found {len(existing_data)} existing records")
            except Exception as e:
                logger.warning(f"⚠️ Could not read existing data: {e}")
                existing_tokens = set()
            
            new_rows = []
            updated_count = 0
            
            for lead in leads_data:
                request_token = lead.get('request_token', '')
                
                # Prepare row data in exact order (55 columns)
                row_data = [
                    lead.get('row_number', ''),
                    lead.get('hub', ''),
                    lead.get('client_name', ''),
                    lead.get('nationality', ''),
                    lead.get('email', ''),
                    lead.get('operator', ''),
                    lead.get('file_status', ''),
                    lead.get('arrival', ''),
                    lead.get('departure', ''),
                    lead.get('pax', ''),
                    lead.get('lead_operation', ''),
                    lead.get('request_channel', ''),
                    lead.get('communication', ''),
                    lead.get('medium', ''),
                    lead.get('offered_income', ''),
                    lead.get('offered_income_usd', ''),
                    lead.get('actual_paid_amount', ''),
                    lead.get('actual_paid_amount_usd', ''),
                    lead.get('remaining_payment', ''),
                    lead.get('remaining_payment_usd', ''),
                    lead.get('submission_date', ''),
                    lead.get('confirmation_date', ''),
                    lead.get('company', ''),
                    lead.get('department', ''),
                    lead.get('product_title', ''),
                    lead.get('utm_campaign', ''),
                    lead.get('initial_price', ''),
                    lead.get('device_type', ''),
                    lead.get('client_phone', ''),
                    lead.get('file_no', ''),
                    lead.get('request_token', ''),
                    lead.get('sales_person', ''),
                    lead.get('request_status', ''),
                    lead.get('source', ''),
                    lead.get('vip_status', ''),
                    lead.get('loyalty_program', ''),
                    lead.get('group', ''),
                    lead.get('has_int_flight', ''),
                    lead.get('single_room', ''),
                    lead.get('double_room', ''),
                    lead.get('triple_room', ''),
                    lead.get('family_room', ''),
                    lead.get('int_flight_amount', ''),
                    lead.get('int_flight_currency', ''),
                    lead.get('agent_group_discount', ''),
                    lead.get('agent_score', ''),
                    lead.get('agent_recommendation', ''),
                    lead.get('ip_country', ''),
                    lead.get('ip_region', ''),
                    lead.get('ip_city', ''),
                    lead.get('profitability_flag', ''),
                    lead.get('communications_count', ''),
                    lead.get('last_updated', ''),
                    lead.get('lead_id', ''),
                    lead.get('lead_url', '')
                ]
                
                if request_token not in existing_tokens:
                    new_rows.append(row_data)
                    updated_count += 1
                    logger.info(f"📝 Prepared new row for: {lead.get('client_name', 'Unknown')}")
            
            # Add new rows to sheet
            if new_rows:
                try:
                    self.sheet.append_rows(new_rows)
                    logger.info(f"✅ Successfully added {len(new_rows)} new rows to Google Sheets")
                except Exception as e:
                    logger.error(f"❌ Failed to append rows: {e}")
                    return 0
            else:
                logger.info("ℹ️ No new leads to add")
            
            return updated_count
            
        except Exception as e:
            logger.error(f"❌ Error syncing to Google Sheets: {e}")
            logger.error(traceback.format_exc())
            return 0
    
    def run_sync(self):
        """Run the complete sync process with comprehensive error handling."""
        try:
            logger.info("=" * 50)
            logger.info("🚀 Starting Memphis Tours ERP Sync")
            logger.info(f"⏰ Execution time: {datetime.now()}")
            logger.info("=" * 50)
            
            # Check prerequisites
            if not self.check_prerequisites():
                logger.error("❌ Prerequisites check failed")
                return False
            
            # Setup Google Sheets
            if not self.setup_google_sheets():
                logger.error("❌ Google Sheets setup failed")
                return False
            
            # Add sample data (in production, this would extract from ERP)
            if not self.add_sample_data_safe():
                logger.error("❌ Data processing failed")
                return False
            
            logger.info("✅ Sync completed successfully!")
            logger.info("=" * 50)
            return True
            
        except Exception as e:
            logger.error(f"❌ Critical error in sync process: {e}")
            logger.error(traceback.format_exc())
            return False

def main():
    """Main function with top-level error handling."""
    try:
        sync_system = RobustMemphisToursSync()
        success = sync_system.run_sync()
        
        if success:
            logger.info("🎉 Memphis Tours sync completed successfully!")
            print("SUCCESS")  # For external monitoring
        else:
            logger.error("💥 Memphis Tours sync failed!")
            print("FAILED")  # For external monitoring
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        logger.error(traceback.format_exc())
        print("FATAL_ERROR")  # For external monitoring
        sys.exit(1)

if __name__ == "__main__":
    main()
