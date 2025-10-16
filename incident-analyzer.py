#!/usr/bin/env python3
"""
PagerDuty Incident Analyzer for ads-demo-service

This script retrieves PagerDuty incidents, correlates them with git commits,
and helps identify root causes.

Usage:
    python incident-analyzer.py --incident-id PXXXXXX
    python incident-analyzer.py --service ads-demo-service --since 2025-10-01
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import urllib.request
import urllib.error


class PagerDutyClient:
    """Client for interacting with PagerDuty API"""
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.pagerduty.com"
        self.headers = {
            "Authorization": f"Token token={api_token}",
            "Accept": "application/vnd.pagerduty+json;version=2",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, endpoint: str) -> Dict[str, Any]:
        """Make a request to the PagerDuty API"""
        url = f"{self.base_url}{endpoint}"
        req = urllib.request.Request(url, headers=self.headers)
        
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            print(f"Error: HTTP {e.code} - {e.reason}")
            return {}
        except urllib.error.URLError as e:
            print(f"Error: {e.reason}")
            return {}
    
    def get_incident(self, incident_id: str) -> Optional[Dict[str, Any]]:
        """Get details for a specific incident"""
        result = self._make_request(f"/incidents/{incident_id}")
        return result.get("incident")
    
    def list_incidents(self, service_name: Optional[str] = None, 
                      since: Optional[str] = None,
                      until: Optional[str] = None,
                      statuses: List[str] = None) -> List[Dict[str, Any]]:
        """List incidents with filters"""
        if statuses is None:
            statuses = ["triggered", "acknowledged"]
        
        params = []
        for status in statuses:
            params.append(f"statuses[]={status}")
        
        if since:
            params.append(f"since={since}")
        if until:
            params.append(f"until={until}")
        
        # Get service ID if service name provided
        if service_name:
            services = self._make_request(f"/services?query={service_name}")
            for service in services.get("services", []):
                if service.get("name") == service_name:
                    params.append(f"service_ids[]={service['id']}")
                    break
        
        query_string = "&".join(params) if params else ""
        result = self._make_request(f"/incidents?{query_string}")
        return result.get("incidents", [])


class GitAnalyzer:
    """Analyze git commits around incident timeframe"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
    
    def get_commits_in_timeframe(self, since: datetime, until: datetime) -> List[Dict[str, str]]:
        """Get commits within a specific timeframe"""
        since_str = since.strftime("%Y-%m-%d %H:%M:%S")
        until_str = until.strftime("%Y-%m-%d %H:%M:%S")
        
        cmd = [
            "git", "-C", self.repo_path, "log",
            f"--since={since_str}",
            f"--until={until_str}",
            "--pretty=format:%H|%an|%ae|%ad|%s",
            "--date=iso"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            commits = []
            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue
                parts = line.split("|", 4)
                if len(parts) == 5:
                    commits.append({
                        "sha": parts[0],
                        "author": parts[1],
                        "email": parts[2],
                        "date": parts[3],
                        "message": parts[4]
                    })
            return commits
        except subprocess.CalledProcessError:
            return []
    
    def get_commit_details(self, commit_sha: str) -> Dict[str, Any]:
        """Get detailed information about a commit"""
        cmd = ["git", "-C", self.repo_path, "show", "--stat", commit_sha]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return {"sha": commit_sha, "details": result.stdout}
        except subprocess.CalledProcessError:
            return {"sha": commit_sha, "details": "Unable to retrieve commit details"}


class IncidentAnalyzer:
    """Analyze incidents and correlate with code changes"""
    
    def __init__(self, pagerduty_client: PagerDutyClient, git_analyzer: GitAnalyzer):
        self.pd_client = pagerduty_client
        self.git_analyzer = git_analyzer
    
    def analyze_incident(self, incident_id: str) -> None:
        """Analyze a specific incident"""
        print(f"Analyzing incident: {incident_id}")
        print("=" * 80)
        
        incident = self.pd_client.get_incident(incident_id)
        if not incident:
            print("Error: Could not retrieve incident")
            return
        
        # Display incident details
        self._display_incident(incident)
        
        # Get timeframe for analysis (24 hours before incident)
        incident_time = datetime.fromisoformat(incident["created_at"].replace("Z", "+00:00"))
        since_time = incident_time - timedelta(hours=24)
        
        print("\n" + "=" * 80)
        print(f"Analyzing commits from {since_time} to {incident_time}")
        print("=" * 80)
        
        # Get commits in timeframe
        commits = self.git_analyzer.get_commits_in_timeframe(since_time, incident_time)
        
        if commits:
            print(f"\nFound {len(commits)} commit(s) in the 24 hours before the incident:")
            print()
            for commit in commits:
                print(f"  SHA: {commit['sha'][:8]}")
                print(f"  Author: {commit['author']} <{commit['email']}>")
                print(f"  Date: {commit['date']}")
                print(f"  Message: {commit['message']}")
                print()
            
            # Analyze the most recent commit
            if commits:
                print("=" * 80)
                print("Most Recent Commit Details:")
                print("=" * 80)
                details = self.git_analyzer.get_commit_details(commits[0]["sha"])
                print(details["details"])
        else:
            print("\nNo commits found in the 24 hours before the incident")
        
        # Provide recommendations
        self._provide_recommendations(incident, commits)
    
    def analyze_service(self, service_name: str, days: int = 7) -> None:
        """Analyze all recent incidents for a service"""
        since = (datetime.now() - timedelta(days=days)).isoformat()
        
        print(f"Analyzing incidents for service: {service_name}")
        print(f"Looking back {days} days from {since}")
        print("=" * 80)
        
        incidents = self.pd_client.list_incidents(
            service_name=service_name,
            since=since
        )
        
        if not incidents:
            print("No incidents found")
            return
        
        print(f"\nFound {len(incidents)} incident(s):\n")
        
        for incident in incidents:
            self._display_incident_summary(incident)
        
        # Analyze patterns
        print("\n" + "=" * 80)
        print("Incident Patterns:")
        print("=" * 80)
        
        by_status = {}
        by_urgency = {}
        
        for incident in incidents:
            status = incident.get("status", "unknown")
            urgency = incident.get("urgency", "unknown")
            by_status[status] = by_status.get(status, 0) + 1
            by_urgency[urgency] = by_urgency.get(urgency, 0) + 1
        
        print("\nBy Status:")
        for status, count in by_status.items():
            print(f"  {status}: {count}")
        
        print("\nBy Urgency:")
        for urgency, count in by_urgency.items():
            print(f"  {urgency}: {count}")
    
    def _display_incident(self, incident: Dict[str, Any]) -> None:
        """Display detailed incident information"""
        print(f"\nIncident #{incident.get('incident_number')} - {incident.get('id')}")
        print(f"Title: {incident.get('title')}")
        print(f"Status: {incident.get('status')}")
        print(f"Urgency: {incident.get('urgency')}")
        print(f"Service: {incident.get('service', {}).get('summary', 'N/A')}")
        print(f"Created: {incident.get('created_at')}")
        print(f"Last Updated: {incident.get('last_status_change_at')}")
        print(f"URL: {incident.get('html_url')}")
        
        description = incident.get("description")
        if description:
            print(f"Description: {description}")
        
        assignments = incident.get("assignments", [])
        if assignments:
            print("\nAssignments:")
            for assignment in assignments:
                assignee = assignment.get("assignee", {})
                print(f"  - {assignee.get('summary')} ({assignee.get('type')})")
    
    def _display_incident_summary(self, incident: Dict[str, Any]) -> None:
        """Display summary of an incident"""
        print(f"  #{incident.get('incident_number')} - {incident.get('status')} - {incident.get('urgency')}")
        print(f"    {incident.get('title')}")
        print(f"    Created: {incident.get('created_at')}")
        print(f"    URL: {incident.get('html_url')}")
        print()
    
    def _provide_recommendations(self, incident: Dict[str, Any], commits: List[Dict[str, str]]) -> None:
        """Provide recommendations based on incident analysis"""
        print("\n" + "=" * 80)
        print("Recommendations:")
        print("=" * 80)
        
        # Check for common issues in the codebase
        description = incident.get("description", "").lower()
        title = incident.get("title", "").lower()
        
        if "oom" in description or "memory" in description or "oomkilled" in title.lower():
            print("\n⚠️  Memory-related incident detected!")
            print("   Potential causes:")
            print("   - Memory leak in application")
            print("   - Insufficient memory limits in Kubernetes deployment")
            print("   - Check worker.c for malloc calls without corresponding free()")
            print("\n   Suggested actions:")
            print("   1. Review memory allocation patterns in worker.c")
            print("   2. Check Kubernetes memory limits in infra/kubernetes/deployment.yaml")
            print("   3. Run memory profiler (valgrind) to identify leaks")
            print("   4. Consider increasing memory limits or fixing the leak")
        
        if commits:
            print(f"\n📝 {len(commits)} commit(s) found in 24h window before incident")
            print("   Suggested actions:")
            print("   1. Review the commits for potentially problematic changes")
            print("   2. Consider rolling back the most recent commit if correlation is strong")
            print("   3. Run tests on the commit before the changes")
        
        print("\n📊 Next Steps:")
        print("   1. Acknowledge the incident in PagerDuty if not already done")
        print("   2. Correlate incident time with deployment times")
        print("   3. Check application logs for error patterns")
        print("   4. Create a fix PR with title: [Incident #{0}] Fix for {1}".format(
            incident.get("incident_number"), incident.get("title")
        ))
        print("   5. Tag on-call team members for review")


def main():
    parser = argparse.ArgumentParser(
        description="PagerDuty Incident Analyzer for ads-demo-service"
    )
    parser.add_argument(
        "--incident-id",
        help="Specific incident ID to analyze"
    )
    parser.add_argument(
        "--service",
        default="ads-demo-service",
        help="Service name (default: ads-demo-service)"
    )
    parser.add_argument(
        "--since",
        help="Look for incidents since date (ISO 8601 format)"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of days to look back (default: 7)"
    )
    
    args = parser.parse_args()
    
    # Get API token from environment
    api_token = os.environ.get("PAGERDUTY_API_TOKEN")
    if not api_token:
        print("Error: PAGERDUTY_API_TOKEN environment variable not set")
        print("Please set it to your PagerDuty API token")
        sys.exit(1)
    
    # Initialize clients
    pd_client = PagerDutyClient(api_token)
    git_analyzer = GitAnalyzer()
    analyzer = IncidentAnalyzer(pd_client, git_analyzer)
    
    # Analyze based on arguments
    if args.incident_id:
        analyzer.analyze_incident(args.incident_id)
    else:
        analyzer.analyze_service(args.service, args.days)


if __name__ == "__main__":
    main()
