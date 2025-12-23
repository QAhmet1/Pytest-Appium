from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Base class to hold common element interactions."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    def find(self, locator):
        """Find element with explicit wait."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        """Wait for element and click."""
        self.find(locator).click()

    def type_text(self, locator, text):
        """Wait for element and send text."""
        self.find(locator).clear()
        self.find(locator).send_keys(text)

    from selenium.webdriver.support import expected_conditions as EC

    def is_visible(self, locator: tuple[str,str], timeout: int = 10) -> bool:
        """
        Checks if an element is physically visible on the screen within the given timeout.

        :param locator: The locator tuple (e.g., AppiumBy.ID, "element_id").
        :param timeout: Maximum time to wait for the element in seconds.
        :return: True if the element is found and visible, False otherwise.
        """
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False