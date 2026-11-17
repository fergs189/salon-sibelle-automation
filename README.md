# Salon SiBelle Automation Testing

Selenium browser automation for [Salon SiBelle](https://www.salonsibelle.ca/) and its linked MySalonOnline booking page.

## User flows

1. **Service availability:** select a service from CSV data and view available appointment times.
2. **Validation recovery:** submit an empty service selection, verify the error, select a valid service on the same form, and view availability.

Both flows stop at availability. No appointment is confirmed.

## Assertions and waits

Each positive case checks:
- The selected service matches the CSV value.
- The availability heading is visible.
- At least one appointment-time option is available.

Negative cases check the exact message `Select a service` and an empty input. Flow 1 has a separate negative case; Flow 2 includes it before correcting the form.

Explicit waits use `WebDriverWait`; there are no fixed sleep timers. A fresh Chrome session is opened for each case. With the supplied three CSV rows, successful execution uses seven browser sessions.

## Files

| File | Purpose |
|---|---|
| test_booking.py | Directly executable Selenium script |
| data/single_services.csv | Three service inputs |
| requirements.txt | Python dependency |
| .gitignore | Excludes local environments and generated files |

## Setup and execution

Install Python 3.10+ and Google Chrome. Open a terminal in this repository's folder.

```bash
python -m pip install -r requirements.txt
python test_booking.py
```

VS Code's **Run Python File** button also works when the selected interpreter has Selenium installed. This is a standalone script; do not use pytest to run it. Selenium Manager resolves ChromeDriver and may need network access on first use.

## Test data

The CSV column is named `service`. Each value must match a booking dropdown option exactly, including spelling, capitalisation, and price. Keep at least three data rows.

## Current limitations and execution status

- The script uses the booking site's default date.
- No available appointments, changed labels, or slow page responses can cause a timeout.
- Dynamic page updates can still cause stale-element failures outside retrying waits.
- Execution stops at the first unhandled failure; browsers are closed in cleanup.
- Successful completion prints no custom messages and generates no HTML report.
- An earlier version's three positive single-service cases passed on the user's computer. The final clean-session version has not been confirmed as fully passing. No passing report is included.
- These are availability and validation-recovery flows, rather than completed bookings. Confirm their scope against the course rubric.

## Repository

https://github.com/fergs189/salon-sibelle-automation
