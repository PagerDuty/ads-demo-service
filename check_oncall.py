#!/usr/bin/env python3
"""
Script to check who is currently on call for PagerDuty teams.
"""

import os
import sys
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def get_pagerduty_api_token():
    """Get PagerDuty API token from environment variable."""
    token = os.environ.get('PAGERDUTY_API_TOKEN')
    if not token:
        print("Error: PAGERDUTY_API_TOKEN environment variable not set", file=sys.stderr)
        print("Please set it with: export PAGERDUTY_API_TOKEN=your_token_here", file=sys.stderr)
        sys.exit(1)
    return token


def make_pagerduty_request(endpoint, api_token):
    """Make a request to PagerDuty API."""
    base_url = "https://api.pagerduty.com"
    url = f"{base_url}{endpoint}"
    
    headers = {
        'Authorization': f'Token token={api_token}',
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'Content-Type': 'application/json'
    }
    
    try:
        request = Request(url, headers=headers)
        with urlopen(request) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        print(f"URL: {url}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"URL Error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def find_team_by_name(team_name, api_token):
    """Find a team by name (case-insensitive partial match)."""
    teams_data = make_pagerduty_request('/teams', api_token)
    
    team_name_lower = team_name.lower()
    for team in teams_data.get('teams', []):
        if team_name_lower in team['name'].lower():
            return team
    
    return None


def get_oncalls_for_team(team_id, api_token):
    """Get current on-call users for a team."""
    endpoint = f'/oncalls?team_ids[]={team_id}'
    oncalls_data = make_pagerduty_request(endpoint, api_token)
    
    return oncalls_data.get('oncalls', [])


def main():
    """Main function to check who's on call for PD Advance Team."""
    # Check for help flag
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("Usage: check_oncall.py [team_name]")
        print()
        print("Check who is currently on call for a PagerDuty team.")
        print()
        print("Examples:")
        print("  check_oncall.py                    # Check PD Advance Team (default)")
        print("  check_oncall.py 'Engineering Team' # Check specific team")
        print()
        print("Required environment variable:")
        print("  PAGERDUTY_API_TOKEN - Your PagerDuty API token")
        sys.exit(0)
    
    # Get API token
    api_token = get_pagerduty_api_token()
    
    # Team name to search for
    team_name = "PD Advance Team"
    if len(sys.argv) > 1:
        team_name = ' '.join(sys.argv[1:])
    
    print(f"Searching for team: {team_name}")
    print("-" * 60)
    
    # Find the team
    team = find_team_by_name(team_name, api_token)
    
    if not team:
        print(f"Error: Team '{team_name}' not found", file=sys.stderr)
        sys.exit(1)
    
    print(f"Found team: {team['name']} (ID: {team['id']})")
    print("-" * 60)
    
    # Get on-call users for the team
    oncalls = get_oncalls_for_team(team['id'], api_token)
    
    if not oncalls:
        print("No one is currently on call for this team.")
        return
    
    print(f"Current on-call engineers for {team['name']}:\n")
    
    for oncall in oncalls:
        user = oncall.get('user', {})
        escalation_policy = oncall.get('escalation_policy', {})
        schedule = oncall.get('schedule', {})
        escalation_level = oncall.get('escalation_level', 'N/A')
        
        print(f"  • {user.get('summary', 'Unknown')}")
        print(f"    Email: {user.get('email', 'N/A')}")
        print(f"    Escalation Policy: {escalation_policy.get('summary', 'N/A')}")
        print(f"    Schedule: {schedule.get('summary', 'N/A')}")
        print(f"    Escalation Level: {escalation_level}")
        print()


if __name__ == "__main__":
    main()
