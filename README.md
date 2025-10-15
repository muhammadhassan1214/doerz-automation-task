Doerz Automation Challenge – Selenium POM
==========================================

A small, focused test automation project that fills out a demo form and verifies a success alert. It uses Python, Selenium, and the Page Object Model (POM) to keep things readable and maintainable.

Project structure
-----------------

- pages/
  - base_page.py – shared helpers for navigation, waits, typing, clicking
  - form_page.py – locators and actions for the challenge page
- tests/
  - test_form_submission.py – data‑driven end‑to‑end test (saves screenshots on failure)
- utils/
  - csv_reader.py – tiny CSV helper
- user_data.csv – input data (First_Name, Last_Name)
- requirements.txt – Python dependencies
- artifacts/ – screenshots captured on failures (auto-created)

What this test does
-------------------

- Opens the challenge page.
- Types first and last name from each row in user_data.csv.
- Clicks a dynamic submit button (its id changes, so we match by prefix: button[id^='submitBtn']).
- Verifies the alert contains the names and then accepts it.

Prerequisites
-------------

- Windows with Python 3.8+ installed and on PATH
- Google Chrome installed

Setup (Windows, cmd)
---------------------

1.  Create or activate a virtual environment (optional but recommended)

        python -m venv .venv
        .venv\Scripts\activate

2.  Install dependencies

        python -m pip install --upgrade pip
        pip install -r requirements.txt

How to run
----------

- Run the test in a headed (visible) Chrome window:

        python tests\test_form_submission.py

- Or run headless (useful for CI or remote environments):

        set HEADLESS=1 && python tests\test_form_submission.py

- Skip E2E (for quick discovery or CI jobs without browser):

        set SKIP_E2E=1 && python -m unittest -v

- Override the base URL (if the page is hosted somewhere else):

        set BASE_URL=https://your-env.example.com/automation_challenge.html && python tests\test_form_submission.py

CSV format
----------

- The CSV must have headers First_Name and Last_Name, for example:

        First_Name,Last_Name
        Ada,Lovelace
        Alan,Turing

Outputs and troubleshooting
---------------------------

- Screenshots on failures are saved under artifacts/screenshots with a timestamped name.
- Chrome/driver version mismatch: webdriver-manager will download a matching driver automatically. If Chrome is very old/new, update it or pin webdriver-manager accordingly.
- Element not clickable/timeouts: rerun, ensure the site is reachable, try headless mode, or increase waits.
- Corporate proxies/SSL interception: configure system proxy or run on an open network.

Design notes
------------

- Page Object Model (POM): interactions live next to locators in pages/, tests stay clean and intent‑focused.
- Robust waits: WebDriverWait is used to reduce flakiness; click and type methods scroll elements into view.
- Dynamic selectors: the submit button id changes; we select it by prefix with CSS: button[id^='submitBtn'].
- Test stability: optional headless mode, sensible Chrome flags, subTest blocks per row, and screenshots on failure.

Next steps (nice-to-haves)
---------------------------

- Add GitHub Actions/CI workflow that runs the test headless and uploads screenshots.
- Add linting/typing (ruff/mypy) for quick feedback in PRs.
- Parameterize timeouts via environment variables.
