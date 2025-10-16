# Example Output

This document shows example output from the `check_oncall.py` script.

## Example 1: Checking PD Advance Team (Default)

```bash
$ export PAGERDUTY_API_TOKEN=your_token_here
$ ./check_oncall.sh
```

**Expected Output:**
```
Searching for team: PD Advance Team
------------------------------------------------------------
Found team: PD Advance Team (ID: PXXXXXX)
------------------------------------------------------------
Current on-call engineers for PD Advance Team:

  • John Smith
    Email: john.smith@example.com
    Escalation Policy: PD Advance Team Escalation Policy
    Schedule: PD Advance Team Primary
    Escalation Level: 1

  • Jane Doe
    Email: jane.doe@example.com
    Escalation Policy: PD Advance Team Escalation Policy
    Schedule: PD Advance Team Secondary
    Escalation Level: 2
```

## Example 2: Checking a Different Team

```bash
$ ./check_oncall.sh "Engineering Team"
```

**Expected Output:**
```
Searching for team: Engineering Team
------------------------------------------------------------
Found team: Engineering Team (ID: PYYYYYY)
------------------------------------------------------------
Current on-call engineers for Engineering Team:

  • Bob Johnson
    Email: bob.johnson@example.com
    Escalation Policy: Engineering Escalation
    Schedule: Engineering On-Call Rotation
    Escalation Level: 1
```

## Example 3: Using Make Command

```bash
$ export PAGERDUTY_API_TOKEN=your_token_here
$ make oncall
```

This is equivalent to running `./check_oncall.sh` directly.

## Example 4: Team Not Found

```bash
$ ./check_oncall.sh "Non-Existent Team"
```

**Expected Output:**
```
Searching for team: Non-Existent Team
------------------------------------------------------------
Error: Team 'Non-Existent Team' not found
```

## Example 5: No One On Call

If no one is currently on call for a team:

```
Searching for team: Example Team
------------------------------------------------------------
Found team: Example Team (ID: PZZZZZZ)
------------------------------------------------------------
No one is currently on call for this team.
```
