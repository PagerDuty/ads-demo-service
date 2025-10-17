#!/usr/bin/env python3
"""
Script to list the last 10 PagerDuty incidents for this service.
"""

import os
import sys
import requests
from datetime import datetime

def list_incidents(api_token=None, service_id=None):
    """
    List the last 10 incidents from PagerDuty.
    
    Args:
        api_token: PagerDuty API token (defaults to PAGERDUTY_API_TOKEN env var)
        service_id: PagerDuty service ID (defaults to PAGERDUTY_SERVICE_ID env var)
    """
    # Get API token from environment or parameter
    api_token = api_token or os.environ.get('PAGERDUTY_API_TOKEN')
    if not api_token:
        print("Error: PAGERDUTY_API_TOKEN environment variable is not set")
        print("Please set it with: export PAGERDUTY_API_TOKEN=your_token_here")
        return 1
    
    # Get service ID from environment or parameter (optional)
    service_id = service_id or os.environ.get('PAGERDUTY_SERVICE_ID')
    
    # Set up API request
    headers = {
        'Authorization': f'Token token={api_token}',
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'Content-Type': 'application/json'
    }
    
    # Build API URL with parameters
    url = 'https://api.pagerduty.com/incidents'
    params = {
        'limit': 10,
        'sort_by': 'created_at:desc',
        'statuses[]': ['triggered', 'acknowledged', 'resolved']
    }
    
    # Add service filter if service_id is provided
    if service_id:
        params['service_ids[]'] = [service_id]
    
    try:
        # Make API request
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        incidents = data.get('incidents', [])
        
        if not incidents:
            print("No incidents found.")
            return 0
        
        print(f"\nLast {len(incidents)} incidents:\n")
        print("=" * 120)
        
        for idx, incident in enumerate(incidents, 1):
            incident_number = incident.get('incident_number', 'N/A')
            title = incident.get('title', 'No title')
            status = incident.get('status', 'unknown')
            urgency = incident.get('urgency', 'unknown')
            created_at = incident.get('created_at', '')
            service_name = incident.get('service', {}).get('summary', 'Unknown service')
            html_url = incident.get('html_url', '')
            
            # Format created_at timestamp
            if created_at:
                try:
                    dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    created_at = dt.strftime('%Y-%m-%d %H:%M:%S UTC')
                except:
                    pass
            
            print(f"{idx}. Incident #{incident_number}")
            print(f"   Title: {title}")
            print(f"   Status: {status.upper()}")
            print(f"   Urgency: {urgency.upper()}")
            print(f"   Service: {service_name}")
            print(f"   Created: {created_at}")
            print(f"   URL: {html_url}")
            
            # Show assignments if available
            assignments = incident.get('assignments', [])
            if assignments:
                assignees = [a.get('assignee', {}).get('summary', 'Unknown') for a in assignments]
                print(f"   Assigned to: {', '.join(assignees)}")
            
            print("-" * 120)
        
        return 0
        
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(list_incidents())
