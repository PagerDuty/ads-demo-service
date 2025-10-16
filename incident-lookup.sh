#!/bin/bash
# PagerDuty Incident Lookup Script for ads-demo-service
# Usage: ./incident-lookup.sh [--incident-id ID] [--service SERVICE_NAME] [--status open|triggered|acknowledged]

set -e

# Configuration
SERVICE_NAME="${PAGERDUTY_SERVICE_NAME:-ads-demo-service}"
PAGERDUTY_API_TOKEN="${PAGERDUTY_API_TOKEN:-}"
PAGERDUTY_API_URL="https://api.pagerduty.com"

# Parse command line arguments
INCIDENT_ID=""
STATUS="triggered,acknowledged"
SINCE=""
UNTIL=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --incident-id)
      INCIDENT_ID="$2"
      shift 2
      ;;
    --service)
      SERVICE_NAME="$2"
      shift 2
      ;;
    --status)
      STATUS="$2"
      shift 2
      ;;
    --since)
      SINCE="$2"
      shift 2
      ;;
    --until)
      UNTIL="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: $0 [OPTIONS]"
      echo "Options:"
      echo "  --incident-id ID    Look up specific incident by ID"
      echo "  --service NAME      Filter by service name (default: ads-demo-service)"
      echo "  --status STATUS     Filter by status: open,triggered,acknowledged,resolved (default: triggered,acknowledged)"
      echo "  --since DATE        Filter incidents since date (ISO 8601 format)"
      echo "  --until DATE        Filter incidents until date (ISO 8601 format)"
      echo ""
      echo "Environment variables:"
      echo "  PAGERDUTY_API_TOKEN    PagerDuty API token (required)"
      echo "  PAGERDUTY_SERVICE_NAME Service name (default: ads-demo-service)"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validate API token
if [ -z "$PAGERDUTY_API_TOKEN" ]; then
  echo "Error: PAGERDUTY_API_TOKEN environment variable is not set"
  echo "Please set it to your PagerDuty API token"
  exit 1
fi

# Function to make PagerDuty API call
pagerduty_api_call() {
  local endpoint=$1
  curl -s -H "Authorization: Token token=${PAGERDUTY_API_TOKEN}" \
       -H "Accept: application/vnd.pagerduty+json;version=2" \
       "${PAGERDUTY_API_URL}${endpoint}"
}

# Function to format incident output
format_incident() {
  local incident=$1
  echo "$incident" | jq -r '
    "================================================================================",
    "Incident #\(.number) - \(.id)",
    "Title: \(.title)",
    "Status: \(.status)",
    "Urgency: \(.urgency)",
    "Service: \(.service.summary)",
    "Created: \(.created_at)",
    "Last Updated: \(.last_status_change_at)",
    "URL: \(.html_url)",
    "Description: \(.description // "N/A")",
    "Assignments:",
    (if .assignments | length > 0 then
      (.assignments[] | "  - \(.assignee.summary) (\(.assignee.type))")
    else
      "  None"
    end),
    "================================================================================",
    ""
  '
}

# Look up specific incident by ID
if [ -n "$INCIDENT_ID" ]; then
  echo "Looking up incident: $INCIDENT_ID"
  echo ""
  incident=$(pagerduty_api_call "/incidents/${INCIDENT_ID}")
  
  if echo "$incident" | jq -e '.incident' > /dev/null 2>&1; then
    format_incident "$(echo "$incident" | jq '.incident')"
    
    # Get recent activity
    echo "Recent Activity:"
    echo "$incident" | jq -r '.incident.log_entries[]? | "  [\(.created_at)] \(.type): \(.summary)"' 2>/dev/null || echo "  No activity logs available"
    echo ""
  else
    echo "Error: Incident not found or API error"
    echo "$incident" | jq '.' 2>/dev/null || echo "$incident"
    exit 1
  fi
  exit 0
fi

# List incidents for the service
echo "Looking up incidents for service: $SERVICE_NAME"
echo "Status filter: $STATUS"
echo ""

# Build query parameters
query_params="statuses[]=${STATUS}"
[ -n "$SINCE" ] && query_params="${query_params}&since=${SINCE}"
[ -n "$UNTIL" ] && query_params="${query_params}&until=${UNTIL}"

# Get service ID first
services=$(pagerduty_api_call "/services?query=${SERVICE_NAME}")
service_id=$(echo "$services" | jq -r ".services[] | select(.name == \"${SERVICE_NAME}\") | .id" | head -1)

if [ -z "$service_id" ]; then
  echo "Warning: Could not find service '${SERVICE_NAME}' in PagerDuty"
  echo "Searching all incidents containing '${SERVICE_NAME}' in the title..."
  incidents=$(pagerduty_api_call "/incidents?${query_params}")
else
  echo "Found service ID: $service_id"
  query_params="${query_params}&service_ids[]=${service_id}"
  incidents=$(pagerduty_api_call "/incidents?${query_params}")
fi

# Check if there are any incidents
incident_count=$(echo "$incidents" | jq '.incidents | length')

if [ "$incident_count" -eq 0 ]; then
  echo "No incidents found matching the criteria"
  exit 0
fi

echo "Found $incident_count incident(s):"
echo ""

# Display each incident
echo "$incidents" | jq -c '.incidents[]' | while read -r incident; do
  format_incident "$incident"
done

# Analyze for patterns
echo ""
echo "=== Incident Analysis ==="
echo "Total incidents: $incident_count"
echo ""
echo "By Status:"
echo "$incidents" | jq -r '.incidents | group_by(.status) | .[] | "  \(.[0].status): \(length)"'
echo ""
echo "By Urgency:"
echo "$incidents" | jq -r '.incidents | group_by(.urgency) | .[] | "  \(.[0].urgency): \(length)"'
echo ""

# Suggest next steps
echo "=== Recommended Actions ==="
echo "1. Review incident timelines to identify patterns"
echo "2. Check recent deployments and correlate with incident creation times"
echo "3. Analyze common error patterns in incident descriptions"
echo "4. Review on-call assignments and ensure proper escalation"
echo ""
echo "To analyze a specific incident in detail:"
echo "  $0 --incident-id <INCIDENT_ID>"
