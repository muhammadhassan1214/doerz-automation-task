Robust POM & Dynamic Wait Challenge (Python + Selenium)
======================================================

Goal
----

- Automate form submission on https://doerz-automation-task.lovable.app/
- Data-driven from user_data.csv (First_Name, Last_Name)
- Use Page Object Model (POM): Pages, Tests, Utils
- Handle dynamic Submit button (ID changes) with a resilient locator + explicit wait

Project structure
-----------------

- pages/
  - base_page.py
  - form_page.py
- tests/
  - test_form_submission.py
- utils/
  - csv_reader.py
- user_data.csv
- requirements.txt

Setup (Windows cmd)
-------------------

1.  Create venv (optional)

        python -m venv .venv
        .venv\Scripts\activate

2.  Install deps

        python -m pip install --upgrade pip
        pip install -r requirements.txt

Run
----

- Execute the test:

        python tests\test_form_submission.py
