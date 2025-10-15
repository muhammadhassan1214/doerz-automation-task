from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    """
    BasePage class that all other page objects will inherit from.
    This class contains common methods for page interactions.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def go_to_url(self, url):
        self.driver.get(url)

    def find_element(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            print(f"Error: Element with locator '{locator}' not found within the wait time.")
            return None

    def click(self, locator):
        try:
            element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(locator))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'nearest'})",
                element,
            )
            element.click()
        except TimeoutException:
            print(f"Error: Element with locator '{locator}' was not clickable within the wait time.")

    def enter_text(self, by_locator, text):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(by_locator))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'nearest'})",
                element,
            )
            field = self.wait.until(EC.visibility_of_element_located(by_locator))
            field.clear()
            field.send_keys(Keys.CONTROL, "a")
            field.send_keys(Keys.BACKSPACE)
            field.send_keys(text)
        except Exception as e:
            print(f"Error entering text into element with locator '{by_locator}': {e}")
