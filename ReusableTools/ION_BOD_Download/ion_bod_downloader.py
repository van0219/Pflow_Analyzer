#!/usr/bin/env python3
"""
ION OneView BOD Downloader
Downloads BOD data objects from ION OneView API for data quality investigations.

This tool is used to:
1. Authenticate via OAuth2 using .ionapi credentials
2. Query the ION OneView /data API to find BODs by document name and date range
3. Download each BOD payload (NDJSON format)
4. Save files locally for analysis

Usage (standalone):
    python ion_bod_downloader.py --ionapi config/IMS.ionapi --doc-name FPI_FCE_IDL_GLTotals \
        --start "2025-12-16T02:49:00.000Z" --end "2025-12-16T03:00:00.000Z"

Usage (via Kiro Agent Hook):
    The agent hook will prompt for parameters and call this script.

API Filter Syntax (from Swagger docs):
- Conditions: (field_name operator 'value')
- Operators: eq, gt, ge, lt, le, range
- Logical: and, or
- Date format: yyyy-MM-dd'T'HH:mm:ss.SSS'Z' (e.g., 2025-12-16T02:00:00.000Z)
"""

import os
import sys
import json
import time
import argparse
import requests
from datetime import datetime

# Default configuration
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "downloads")
DEFAULT_CONFIG_DIR = os.path.join(os.path.dirname(__file__), "config")
RECORDS_PER_PAGE = 100
REQUEST_TIMEOUT = 60


def load_ionapi_credentials(ionapi_path):
    """Load OAuth2 credentials from .ionapi file."""
    with open(ionapi_path, 'r') as f:
        creds = json.load(f)
    
    # Extract required fields
    tenant = creds.get('ti', '')
    
    # Note: saak and ci fields already contain the tenant prefix (ti# and ti~)
    # Do NOT add the prefix again!
    return {
        'tenant': tenant,
        'token_url': f"https://mingle-sso.inforcloudsuite.com:443/{tenant}/as/token.oauth2",
        'api_base_url': f"https://mingle-ionapi.inforcloudsuite.com/{tenant}",
        'username': creds.get('saak', ''),      # saak already has ti# prefix
        'password': creds.get('sask', ''),
        'client_id': creds.get('ci', ''),       # ci already has ti~ prefix
        'client_secret': creds.get('cs', '')
    }


def get_access_token(creds):
    """Get OAuth2 access token."""
    payload = {
        'grant_type': 'password',
        'username': creds['username'],
        'password': creds['password'],
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret']
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    
    print(f"Authenticating to {creds['token_url']}...")
    response = requests.post(creds['token_url'], data=payload, headers=headers, timeout=REQUEST_TIMEOUT)
    
    if response.status_code != 200:
        print(f"Authentication failed: {response.status_code}")
        print(response.text)
        return None
    
    token_data = response.json()
    print("Authentication successful!")
    return token_data['access_token']


def build_filter_query(doc_name, start_date, end_date, source_filter="lid://infor.bice.bice"):
    """Build the filter query for BODs in the date range."""
    filter_parts = []
    
    # Only add source filter if it's a valid value (not empty, "none", or "skip")
    if source_filter and source_filter.lower() not in ('none', 'skip', ''):
        filter_parts.append(f"(document_sent_from eq '{source_filter}')")
    
    if doc_name:
        filter_parts.append(f"(document_name eq '{doc_name}')")
    
    if start_date and end_date:
        filter_parts.append(f"message_date range [{start_date}, {end_date}]")
    
    return " and ".join(filter_parts)


def get_message_list(creds, access_token, doc_name, start_date, end_date, page=1):
    """Query the /data API to get list of messages with MessageIDs."""
    endpoint = f"{creds['api_base_url']}/IONSERVICES/oneviewapi/data"
    
    # Build filter query string
    filter_parts = []
    if doc_name:
        filter_parts.append(f"(document_type eq '{doc_name}')")
    if start_date and end_date:
        filter_parts.append(f"message_date range [{start_date}, {end_date}]")
    filter_query = " and ".join(filter_parts)
    
    params = {
        'filter': filter_query,
        'store': 'Message',
        'page': page,
        'records': RECORDS_PER_PAGE,
        'sort': 'message_date:asc'
    }
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }
    
    print(f"  Querying page {page}...")
    print(f"  Filter: {filter_query}")
    response = requests.get(endpoint, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
    
    if response.status_code != 200:
        print(f"Query failed: {response.status_code}")
        print(response.text)
        return None
    
    return response.json()


def download_bod_payload(creds, access_token, message_id, output_path):
    """Download a single BOD payload by MessageID."""
    endpoint = f"{creds['api_base_url']}/IONSERVICES/oneviewapi/data/streamDocumentPayload"
    
    params = {'messageId': message_id}
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': '*/*'
    }
    
    response = requests.get(endpoint, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
    
    if response.status_code != 200:
        # Try documentPayload with text/xml as fallback
        endpoint = f"{creds['api_base_url']}/IONSERVICES/oneviewapi/data/documentPayload"
        headers['Accept'] = 'text/xml'
        response = requests.get(endpoint, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
        
        if response.status_code != 200:
            return False
    
    with open(output_path, 'wb') as f:
        f.write(response.content)
    
    return True


def download_bods(ionapi_path, doc_name, start_date, end_date, output_dir, source_filter="lid://infor.bice.bice"):
    """Main function to download all BODs matching the criteria."""
    print("=" * 70)
    print("ION OneView BOD Downloader")
    print("=" * 70)
    print(f"Credentials: {ionapi_path}")
    print(f"Document Name: {doc_name}")
    print(f"Date Range: {start_date} to {end_date}")
    print(f"Source Filter: {source_filter}")
    print(f"Output: {output_dir}")
    print("=" * 70)
    
    # Load credentials
    creds = load_ionapi_credentials(ionapi_path)
    print(f"Tenant: {creds['tenant']}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Get access token
    access_token = get_access_token(creds)
    if not access_token:
        return {'success': False, 'error': 'Authentication failed'}
    
    # Get first page to determine total count
    print("\n" + "-" * 70)
    print("Step 1: Querying for MessageIDs...")
    print("-" * 70)
    
    result = get_message_list(creds, access_token, doc_name, start_date, end_date, page=1)
    
    if not result:
        return {'success': False, 'error': 'Failed to query messages'}
    
    total_found = result.get('numFound', 0)
    print(f"Total BODs found: {total_found}")
    
    if total_found == 0:
        print("No BODs found matching the filter criteria.")
        return {'success': True, 'total': 0, 'downloaded': 0, 'failed': 0}
    
    # Collect all MessageIDs
    all_messages = []
    page = 1
    
    while True:
        if page > 1:
            result = get_message_list(creds, access_token, doc_name, start_date, end_date, page=page)
            if not result:
                break
        
        messages = result.get('fields', []) or result.get('objectList', [])
        if not messages:
            break
        
        all_messages.extend(messages)
        print(f"  Retrieved {len(all_messages)} / {total_found} messages")
        
        if len(all_messages) >= total_found:
            break
        
        page += 1
        time.sleep(0.5)
    
    # Extract MessageIDs
    message_ids = []
    for msg in all_messages:
        msg_id = msg.get('message_id') or msg.get('messageId') or msg.get('id')
        if msg_id:
            message_ids.append({
                'message_id': msg_id,
                'document_type': msg.get('document_type', ''),
                'message_date': msg.get('message_date', ''),
                'document_size': msg.get('document_size', 0)
            })
    
    # Save MessageID list
    list_file = os.path.join(output_dir, 'message_ids.json')
    with open(list_file, 'w') as f:
        json.dump(message_ids, f, indent=2)
    print(f"\nMessageID list saved to: {list_file}")
    
    # Download each BOD
    print("\n" + "-" * 70)
    print("Step 2: Downloading BOD payloads...")
    print("-" * 70)
    
    success_count = 0
    fail_count = 0
    
    for i, msg_info in enumerate(message_ids, 1):
        msg_id = msg_info['message_id']
        
        safe_id = msg_id.replace('/', '_').replace('\\', '_').replace(':', '_')
        if len(safe_id) > 100:
            safe_id = safe_id[:100]
        output_file = os.path.join(output_dir, f"bod_{i:04d}_{safe_id}.json")
        
        print(f"[{i}/{len(message_ids)}] Downloading...")
        
        if download_bod_payload(creds, access_token, msg_id, output_file):
            success_count += 1
        else:
            fail_count += 1
        
        if i % 10 == 0:
            time.sleep(1)
        else:
            time.sleep(0.2)
    
    # Summary
    print("\n" + "=" * 70)
    print("DOWNLOAD COMPLETE")
    print("=" * 70)
    print(f"Total BODs found: {total_found}")
    print(f"Successfully downloaded: {success_count}")
    print(f"Failed: {fail_count}")
    print(f"Output directory: {output_dir}")
    
    return {
        'success': True,
        'total': total_found,
        'downloaded': success_count,
        'failed': fail_count,
        'output_dir': output_dir
    }


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description='Download BODs from ION OneView API')
    parser.add_argument('--ionapi', required=True, help='Path to .ionapi credentials file')
    parser.add_argument('--doc-name', help='Document name filter (e.g., FPI_FCE_IDL_GLTotals)')
    parser.add_argument('--start', required=True, help='Start datetime (UTC, format: YYYY-MM-DDTHH:MM:SS.sssZ)')
    parser.add_argument('--end', required=True, help='End datetime (UTC, format: YYYY-MM-DDTHH:MM:SS.sssZ)')
    parser.add_argument('--output', default=DEFAULT_OUTPUT_DIR, help='Output directory for downloaded BODs')
    parser.add_argument('--source', default='lid://infor.bice.bice', help='Source filter (default: lid://infor.bice.bice)')
    
    args = parser.parse_args()
    
    result = download_bods(
        ionapi_path=args.ionapi,
        doc_name=args.doc_name,
        start_date=args.start,
        end_date=args.end,
        output_dir=args.output,
        source_filter=args.source
    )
    
    return 0 if result.get('success') else 1


if __name__ == "__main__":
    sys.exit(main())
