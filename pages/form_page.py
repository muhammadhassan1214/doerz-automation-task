from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException

from pages.base_page import BasePage


class FormPage(BasePage):
    """Page object for the automation challenge form page."""

    # Locators
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, "input#firstName")
    LAST_NAME_INPUT = (By.CSS_SELECTOR, "input#lastName")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[id^='submitBtn']")

    def __init__(self, driver):
        super(FormPage, self).__init__(driver)
        self.url = "https://doerz-automation-task.lovable.app/automation_challenge.html"

    def load(self):
        self.go_to_url(self.url)

    def enter_first_name(self, first_name):
        self.enter_text(self.FIRST_NAME_INPUT, first_name)

    def enter_last_name(self, last_name):
        self.enter_text(self.LAST_NAME_INPUT, last_name)

    def click_submit(self):
        self.click(self.SUBMIT_BUTTON)

    def handle_and_verify_success_alert(self, first_name, last_name):
        try:
            self.wait.until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text

            expected_line1 = "Form Submitted Successfully!"
            expected_line2 = f"First Name: {first_name}"
            expected_line3 = f"Last Name: {last_name}"

            is_text_correct = (
                expected_line1 in alert_text and
                expected_line2 in alert_text and
                expected_line3 in alert_text
            )

            alert.accept()

            if not is_text_correct:
                print(f"Alert text mismatch! Got: '{alert_text}'")

            return is_text_correct
        except (TimeoutException, NoAlertPresentException):
            print("Error: Success alert did not appear within the wait time.")
            return False

    def fill_and_submit_form(self, first_name, last_name):
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.click_submit()
