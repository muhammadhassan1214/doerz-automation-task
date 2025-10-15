import unittest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from pages.form_page import FormPage
from utils.csv_reader import read_csv_data


class TestFormSubmission(unittest.TestCase):
    """Submit the form for each row in user_data.csv and verify the alert."""

    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.implicitly_wait(5)
        self.form_page = FormPage(self.driver)

    def test_submit_form_with_csv_data(self):
        users = read_csv_data("user_data.csv")
        self.assertIsNotNone(users, "Failed to read user data from CSV.")
        self.assertGreater(len(users), 0, "CSV has no rows to test.")

        for user in users:
            with self.subTest(user=user):
                self.form_page.load()
                first_name = user["First_Name"].strip()
                last_name = user["Last_Name"].strip()
                self.form_page.fill_and_submit_form(first_name, last_name)
                ok = self.form_page.handle_and_verify_success_alert(first_name, last_name)
                self.assertTrue(ok, f"Submission failed for {first_name} {last_name}")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
