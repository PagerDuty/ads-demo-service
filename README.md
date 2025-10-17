# Demo service to test ADS

Testing

## PagerDuty Incident Management

### List Last 10 Incidents

To list the last 10 incidents from PagerDuty, use the `list_incidents.py` script:

**Quick Start (using shell script):**
```bash
# Set your PagerDuty API token
export PAGERDUTY_API_TOKEN=your_token_here

# Optional: Set specific service ID to filter incidents
export PAGERDUTY_SERVICE_ID=your_service_id

# Run the script
./list_incidents.sh
```

**Or use Python directly:**
```bash
# Install dependencies first
pip install -r requirements.txt

# Run the script
python3 list_incidents.py
```

**Or use Makefile:**
```bash
make install-deps
make list-incidents
```

**Requirements:**
- Python 3.6+
- `requests` library: `pip install requests`

**Environment Variables:**
- `PAGERDUTY_API_TOKEN` (required): Your PagerDuty API token
- `PAGERDUTY_SERVICE_ID` (optional): Filter incidents by specific service ID

The script will display the last 10 incidents including:
- Incident number and title
- Status (triggered, acknowledged, resolved)
- Urgency level
- Service name
- Creation timestamp
- PagerDuty URL
- Assigned team members
