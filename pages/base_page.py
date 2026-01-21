from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Base class to hold common element interactions."""

    def __init__(self, driver):
        self.driver = driver
        # Keep default explicit wait at a reasonable value
        # Too high values slow down tests a lot when locators are wrong.
        self.wait = WebDriverWait(self.driver, 10)

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

    def get_text(self, locator):
        """
        Waits for the element to be visible, then retrieves its text content.
        :param locator: Tuple (By.ID, "value") or similar.
        :return: String value of the element's text.
        """
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.text

    def is_visible(self, locator: tuple[str, str], timeout: int = 10) -> bool:
        """
        Checks if an element is physically visible on the screen within the given timeout.

        :param locator: The locator tuple (e.g., AppiumBy.ID, "element_id").
        :param timeout: Maximum time to wait for the element in seconds.
        :return: True if the element is found and visible, False otherwise.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def verify_element_text(self, locator, expected_text):
        """
        Retrieves the text from the given locator and asserts it matches the expected text.
        :param locator: The element locator (tuple).
        :param expected_text: The string value we expect to find.
        """
        actual_text = self.get_text(locator)  # Assuming get_text is defined in your BasePage
        assert actual_text == expected_text, f"Expected: '{expected_text}', but found: '{actual_text}'"

    def clear_input_field(self, locator):
        """
        Waits for the element to be visible and clears its text content.
        :param locator: The element locator (tuple).
        """
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()