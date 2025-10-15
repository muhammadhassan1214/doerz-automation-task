from __future__ import annotations

import logging
import os
from typing import Tuple

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class FormPage(BasePage):
    """
    Page Object representing the form page for the automation challenge.
    Encapsulates locators and user actions on that page.
    """

    # Locators
    FIRST_NAME_INPUT: Tuple[str, str] = (By.CSS_SELECTOR, "input#firstName")
    LAST_NAME_INPUT: Tuple[str, str] = (By.CSS_SELECTOR, "input#lastName")

    # The submit button's id changes dynamically but always starts with 'submitBtn'.
    SUBMIT_BUTTON: Tuple[str, str] = (By.CSS_SELECTOR, "button[id^='submitBtn']")

    def __init__(self, driver) -> None:
        super().__init__(driver)
        default_url = "https://doerz-automation-task.lovable.app/automation_challenge.html"
        self.url = os.getenv("BASE_URL", default_url)

    def load(self) -> None:
        """Open the form page."""
        self.go_to_url(self.url)

    def enter_first_name(self, first_name: str) -> None:
        """Type into the first name input."""
        self.enter_text(self.FIRST_NAME_INPUT, first_name)

    def enter_last_name(self, last_name: str) -> None:
        """Type into the last name input."""
        self.enter_text(self.LAST_NAME_INPUT, last_name)

    def click_submit(self) -> None:
        """Click the dynamic submit button."""
        self.click(self.SUBMIT_BUTTON)

    def handle_and_verify_success_alert(self, first_name: str, last_name: str) -> bool:
        """
        Wait for the alert, validate its text, and accept it.

        Returns:
            True if the alert text contains all expected lines; False otherwise.
        """
        try:
            # Wait for the alert to be present and then switch to it
            self.wait.until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text

            expected_line1 = "Form Submitted Successfully!"
            expected_line2 = f"First Name: {first_name}"
            expected_line3 = f"Last Name: {last_name}"

            is_text_correct = (
                expected_line1 in alert_text
                and expected_line2 in alert_text
                and expected_line3 in alert_text
            )

            # Close the alert regardless of check outcome
            alert.accept()

            if not is_text_correct:
                logger.warning("Alert text mismatch. Got: %r", alert_text)

            return is_text_correct

        except (TimeoutException, NoAlertPresentException):
            logger.error("Success alert did not appear within the wait time.")
            return False

    def fill_and_submit_form(self, first_name: str, last_name: str) -> None:
        """Fill both inputs and submit the form."""
        logger.info("Submitting form for: %s %s", first_name, last_name)
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.click_submit()
