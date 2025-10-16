# Demo service to test ADS

Testing

## PagerDuty On-Call Checker

This repository includes a script to check who is currently on call for PagerDuty teams.

### Usage

1. Set your PagerDuty API token as an environment variable:
   ```bash
   export PAGERDUTY_API_TOKEN=your_token_here
   ```

2. Run the script to check who's on call for the PD Advance Team:
   ```bash
   ./check_oncall.sh
   ```
   
   Or use the Python script directly:
   ```bash
   python3 check_oncall.py
   ```

3. Or check a different team by passing the team name as an argument:
   ```bash
   ./check_oncall.sh "Team Name"
   ```

### Getting a PagerDuty API Token

1. Log in to your PagerDuty account
2. Go to **User Icon** → **My Profile** → **User Settings**
3. Click on **Create API User Token**
4. Copy the token and set it as the `PAGERDUTY_API_TOKEN` environment variable
