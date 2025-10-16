# Demo service to test ADS

Testing

## PagerDuty Integration

### List Open Incidents

This repository includes a script to list all open incidents from PagerDuty.

#### Prerequisites
- Python 3.x
- PagerDuty API token

#### Usage

1. Set your PagerDuty API token as an environment variable:
```bash
export PAGERDUTY_API_TOKEN='your-api-token-here'
```

2. Run the script:
```bash
python3 list_incidents.py
```

Or make it executable and run directly:
```bash
chmod +x list_incidents.py
./list_incidents.py
```

#### Output

The script will display all open (triggered or acknowledged) incidents with the following information:
- Incident number and ID
- Title
- Status (triggered/acknowledged)
- Urgency (high/low)
- Service name
- Created timestamp

#### Example Output
```
Fetching open incidents from PagerDuty...

Found 2 open incident(s):

============================================================
Incident #123 (PXXXXXX)
  Title: High CPU usage on production server
  Status: triggered
  Urgency: high
  Service: Production API
  Created: 2025-10-16T14:30:00Z
------------------------------------------------------------
Incident #124 (PYYYYYY)
  Title: Database connection timeout
  Status: acknowledged
  Urgency: high
  Service: Database Cluster
  Created: 2025-10-16T14:35:00Z
------------------------------------------------------------
```
