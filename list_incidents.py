#!/usr/bin/env python3
"""
PagerDuty Incident Lister
This script lists all open incidents from PagerDuty using the REST API.
"""

import os
import sys
import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def list_open_incidents(api_token):
    """
    List all open incidents from PagerDuty.
    
    Args:
        api_token (str): PagerDuty API token
        
    Returns:
        list: List of open incidents
    """
    url = "https://api.pagerduty.com/incidents"
    headers = {
        "Authorization": f"Token token={api_token}",
        "Accept": "application/vnd.pagerduty+json;version=2",
        "Content-Type": "application/json"
    }
    
    # Parameters to filter for open incidents
    params = "?statuses[]=triggered&statuses[]=acknowledged"
    full_url = url + params
    
    try:
        request = Request(full_url, headers=headers)
        with urlopen(request) as response:
            data = json.loads(response.read().decode())
            return data.get("incidents", [])
    except HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}", file=sys.stderr)
        if e.code == 401:
            print("Authentication failed. Please check your API token.", file=sys.stderr)
        elif e.code == 403:
            print("Access forbidden. Please check your API token permissions.", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"URL Error: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


def format_incident(incident):
    """
    Format incident data for display.
    
    Args:
        incident (dict): Incident data
        
    Returns:
        str: Formatted incident string
    """
    incident_id = incident.get("id", "N/A")
    incident_number = incident.get("incident_number", "N/A")
    title = incident.get("title", "N/A")
    status = incident.get("status", "N/A")
    urgency = incident.get("urgency", "N/A")
    created_at = incident.get("created_at", "N/A")
    
    service = incident.get("service", {})
    service_name = service.get("summary", "N/A") if service else "N/A"
    
    return (
        f"Incident #{incident_number} ({incident_id})\n"
        f"  Title: {title}\n"
        f"  Status: {status}\n"
        f"  Urgency: {urgency}\n"
        f"  Service: {service_name}\n"
        f"  Created: {created_at}\n"
    )


def main():
    """Main function to list and display open PagerDuty incidents."""
    # Get API token from environment variable
    api_token = os.environ.get("PAGERDUTY_API_TOKEN")
    
    if not api_token:
        print("Error: PAGERDUTY_API_TOKEN environment variable is not set.", file=sys.stderr)
        print("\nUsage:", file=sys.stderr)
        print("  export PAGERDUTY_API_TOKEN='your-api-token-here'", file=sys.stderr)
        print("  python3 list_incidents.py", file=sys.stderr)
        sys.exit(1)
    
    print("Fetching open incidents from PagerDuty...\n")
    
    incidents = list_open_incidents(api_token)
    
    if not incidents:
        print("No open incidents found.")
        return
    
    print(f"Found {len(incidents)} open incident(s):\n")
    print("=" * 60)
    
    for incident in incidents:
        print(format_incident(incident))
        print("-" * 60)


if __name__ == "__main__":
    main()
