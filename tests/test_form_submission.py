import os
import unittest
import logging
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from pages.form_page import FormPage
from utils.csv_reader import read_csv_data


@unittest.skipIf(os.getenv("SKIP_E2E") == "1", "E2E tests are skipped by SKIP_E2E=1")
class TestFormSubmission(unittest.TestCase):
    """End-to-end tests for the form submission flow."""

    def setUp(self):
        """
        Prepare a fresh browser for each test.
        Uses webdriver_manager to provision the matching chromedriver.
        """
        # Configure logging once to surface page object info during runs.
        root_logger = logging.getLogger()
        if not root_logger.handlers:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s %(levelname)s %(name)s: %(message)s",
            )

        options = ChromeOptions()
        # Enable headless mode if HEADLESS=1 is set (useful for CI)
        if os.getenv("HEADLESS", "0") == "1":
            options.add_argument("--headless=new")
        # Stability flags (harmless locally, helpful in CI/containers)
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,900")

        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options,
        )
        self.driver.implicitly_wait(5)
        self.form_page = FormPage(self.driver)

    def test_submit_form_with_csv_data(self):
        """
        Read rows from user_data.csv and submit the form for each one.
        Verify the success alert contains the provided names.
        """
        users = read_csv_data("user_data.csv")
        self.assertIsNotNone(users, "Failed to read user data from CSV.")
        self.assertGreater(len(users), 0, "CSV has no rows to test.")

        for user in users:
            with self.subTest(user=user):
                self.form_page.load()

                first_name = user["First_Name"].strip()
                last_name = user["Last_Name"].strip()

                self.form_page.fill_and_submit_form(first_name, last_name)

                is_successful = self.form_page.handle_and_verify_success_alert(first_name, last_name)
                self.assertTrue(
                    is_successful,
                    msg=f"Submission failed or alert mismatch for '{first_name} {last_name}'",
                )

    def tearDown(self):
        """Close the browser. If the test failed, save a screenshot to artifacts/screenshots."""
        try:
            # Determine if this test had an error or failure
            failed = False
            outcome = getattr(self, "_outcome", None)
            if outcome is not None:
                result = getattr(outcome, "result", None)
                if result is not None:
                    errors = list(result.errors) + list(result.failures)
                else:
                    errors = list(getattr(outcome, "errors", []))
                failed = any(err for (_test, err) in errors if err)

            if failed and hasattr(self, "driver"):
                ts = datetime.now().strftime("%Y%m%d-%H%M%S")
                out_dir = Path("artifacts") / "screenshots"
                out_dir.mkdir(parents=True, exist_ok=True)
                filename = out_dir / f"{self._testMethodName}_{ts}.png"
                self.driver.save_screenshot(str(filename))
                logging.getLogger(__name__).info("Saved failure screenshot: %s", filename)
        finally:
            if hasattr(self, "driver"):
                self.driver.quit()


if __name__ == "__main__":
    unittest.main()
