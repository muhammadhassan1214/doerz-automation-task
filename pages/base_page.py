from __future__ import annotations

import logging
from typing import Optional, Tuple

from selenium.webdriver import Keys, Remote
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Configure a module-level logger (library-style: don't add handlers here)
logger = logging.getLogger(__name__)


class BasePage:
    """
    BasePage class that all other page objects will inherit from.
    This class contains common methods for page interactions.
    """

    def __init__(self, driver: Remote, default_timeout: int = 10) -> None:
        """
        Initialize the BasePage with a WebDriver instance.

        Args:
            driver: Selenium WebDriver instance.
            default_timeout: Explicit wait timeout in seconds.
        """
        self.driver: Remote = driver
        self.wait = WebDriverWait(self.driver, default_timeout)

    def go_to_url(self, url: str) -> None:
        """
        Navigate to the specified URL.
        """
        self.driver.get(url)

    def find_element(self, locator: Tuple[str, str]) -> Optional[WebElement]:
        """
        Find and return a web element after waiting for it to be visible.

        Args:
            locator: Tuple(By, selector) for the target element.

        Returns:
            The visible WebElement if found within timeout, otherwise None.
        """
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            logger.error("Element not found within wait time: %s", locator)
            return None

    def click(self, locator: Tuple[str, str]) -> None:
        """
        Wait for an element to be clickable and then click it.
        """
        try:
            element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(locator))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'nearest'})",
                element,
            )
            element.click()
        except TimeoutException:
            logger.error("Element not clickable within wait time: %s", locator)

    def enter_text(self, by_locator: Tuple[str, str], text: str) -> None:
        """
        Find an element, clear its content, and enter the given text.
        """
        try:
            element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(by_locator))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'nearest'})",
                element,
            )
            field = self.wait.until(EC.visibility_of_element_located(by_locator))
            # Try a standard clear, then ensure it's empty by select-all + backspace
            field.clear()
            field.send_keys(Keys.CONTROL, "a")
            field.send_keys(Keys.BACKSPACE)
            # Type the new value
            field.send_keys(text)
        except Exception as e:  # noqa: BLE001 - broad for UI robustness
            logger.exception("Error entering text into %s: %s", by_locator, e)
