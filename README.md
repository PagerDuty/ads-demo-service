# Demo service to test ADS

Testing

## Incident Response

This repository includes tools for looking up and analyzing PagerDuty incidents related to the ads-demo-service.

### Quick Start

1. Set your PagerDuty API token:
   ```bash
   export PAGERDUTY_API_TOKEN="your-token-here"
   ```

2. Look up incidents:
   ```bash
   # Using the bash script (quick lookup)
   ./incident-lookup.sh --service ads-demo-service
   
   # Using the Python analyzer (detailed analysis with git correlation)
   python3 incident-analyzer.py --incident-id PXXXXXX
   ```

### Available Tools

- **incident-lookup.sh**: Quick incident lookup using PagerDuty API
- **incident-analyzer.py**: Detailed incident analysis with git commit correlation
- **test-incident-tools.sh**: Test script to verify tools are working
- **INCIDENT_RESPONSE.md**: Complete incident response guide
- **EXAMPLE_USAGE.md**: Examples with sample outputs

See [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md) for detailed usage instructions and incident response workflows.

See [EXAMPLE_USAGE.md](EXAMPLE_USAGE.md) for example commands and outputs.

## Known Issues

The worker.c application has a memory leak that will cause OOMKilled incidents. See INCIDENT_RESPONSE.md for details on identifying and fixing memory-related incidents.
