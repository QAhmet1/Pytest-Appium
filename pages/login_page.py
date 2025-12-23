import json
import os

from appium.webdriver.common.appiumby import AppiumBy  # Correct import for Appium locators
from selenium.common import NoSuchElementException

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Sign In screen Page Object.

    Contains ONLY locators and user-level actions.
    All test logic must live under `tests/`.
    """

    # --- Locators ---
    # We use AppiumBy for Mobile-specific selectors
    SIGN_IN_BUTTON_ONBOARDING = (AppiumBy.ACCESSIBILITY_ID, "Sign in")
    SIGNIN_TITLE = (AppiumBy.ID, "login_title_text")
    # Use full Android resource-id values for more reliable lookup
    EMAIL_INPUT = (AppiumBy.XPATH, "//android.widget.EditText[@resource-id='login_email_input']")
    PASSWORD_INPUT = (AppiumBy.XPATH, "//android.widget.EditText[@resource-id='login_password_input']")
    LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Continue")
    REQUIRED_FIELD_ERRORS_1 = (AppiumBy.XPATH, "(//android.widget.TextView[@text='This field is required'])[1]")
    REQUIRED_FIELD_ERRORS_2 = (AppiumBy.XPATH, "(//android.widget.TextView[@text='This field is required'])[2]")
    REQUIRED_ERROR_MESSAGE = (AppiumBy.XPATH,"//android.widget.TextView[@text='This field is required']")

    # Accessibility IDs for cross-platform (iOS/Android) compatibility
    MAYBE_LATER_BTN = (AppiumBy.ACCESSIBILITY_ID, "Maybe later")
    NOTIFY_ME_BTN = (AppiumBy.ACCESSIBILITY_ID, "Yes, notify me")

    # Complex selectors like WDIO's android=new UiSelector()
    INVALID_FORMAT_ERROR = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Must be a valid email format")',
    )
    PORTFOLIO_TAB = (AppiumBy.ID, "portfolio_tab")

    # --- Actions ---
    def navigate_to_signin_screen(self):
        """Ensure we are on the Sign in screen.

        If the onboarding Sign in button exists, tap it; otherwise assume
        we are already on the login screen and just wait for the title.
        """

        if self.is_visible(self.SIGN_IN_BUTTON_ONBOARDING,timeout=5):
            self.click(self.SIGN_IN_BUTTON_ONBOARDING)

        is_on_login_page = self.is_visible(self.EMAIL_INPUT,timeout=10)
        assert is_on_login_page is True,"Navigation failed: Login scree(Email input) not found."


    def login(self, email: str, password: str):
        """Main login method."""
        # self.navigate_to_signin_screen()
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def handle_notification_prompt(self):
        """Handles post-login dismissible buttons and system notifications."""
        try:
            # Safe click
            self.click(self.MAYBE_LATER_BTN)
        except NoSuchElementException:
            # Optional info log – do not fail test because of missing prompt
            print("Maybe Later button not found, continuing flow.")

        try:
            self.click(self.NOTIFY_ME_BTN)
            # For native alerts in Appium:
            self.driver.switch_to.alert.accept()
        except NoSuchElementException:
            print("Notification prompt did not appear.")


    def verify_required_field_visible(self):
        """Verify that the first 'This field is required' error is visible."""
        assert self.is_visible(self.REQUIRED_ERROR_MESSAGE), "The required field error message is not visible!"

    def verify_credentials_required_field_visible_1(self):
        """Verify that the first 'This field is required' error is visible."""
        assert self.is_visible(self.REQUIRED_FIELD_ERRORS_1), "The email required field error message is not visible!"


    def verify_credentials_required_field_visible_2(self):
        """Verify that the second 'This field is required' error is visible."""
        assert self.is_visible(self.REQUIRED_FIELD_ERRORS_2), "The password required field error message is not visible!"
