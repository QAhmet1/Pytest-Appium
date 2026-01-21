import json
import os

from appium.webdriver.common.appiumby import AppiumBy  # Correct import for Appium locators
from selenium.common import NoSuchElementException, TimeoutException

from pages.base_page import BasePage
from utils.constants import UIConstants


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
    WRONG_EMAIL_FORMAT_MESSAGE =(AppiumBy.XPATH,"//android.widget.TextView[@text='Must be a valid email format']")
    WRONG_EMAIL_OR_PASSWORD_MESSAGE =(AppiumBy.XPATH,"//android.widget.TextView[@resource-id='login_error']") #TEXT="Your email or password is incorrect"
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
        we are already on the login screen and just wait for the email field.
        """
        # If we already navigated once in this driver session, skip all checks.
        if getattr(self.driver, "_onboarding_done", False):
            return

        # Fast path: if we are already on the login screen, return immediately.
        if self.is_visible(self.EMAIL_INPUT, timeout=2):
            # Mark onboarding as done for this session
            self.driver._onboarding_done = True
            return

        # On first launch there might be an onboarding "Sign in" button.
        # If it is not present, we simply continue.
        try:
            if self.is_visible(self.SIGN_IN_BUTTON_ONBOARDING, timeout=3):
                self.click(self.SIGN_IN_BUTTON_ONBOARDING)
        except (TimeoutException, NoSuchElementException):
            # Onboarding did not appear or disappeared during wait – continue.
            pass

        # In all cases, make sure the email input of the login screen is visible.
        is_on_login_page = self.is_visible(self.EMAIL_INPUT, timeout=7)
        assert (
            is_on_login_page is True
        ), "Navigation failed: Login screen (Email input) not found."

        # Mark onboarding as completed so subsequent tests skip navigation.
        self.driver._onboarding_done = True


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

    def verify_wrong_email_format_message(self):
        """Verify that the second 'This field is required' error is visible."""
        assert self.is_visible(self.WRONG_EMAIL_FORMAT_MESSAGE), "The password required field error message is not visible!"
        self.verify_element_text(self.WRONG_EMAIL_FORMAT_MESSAGE,UIConstants.INVALID_EMAIL_FORMAT)

    def verify_wrong_password(self):
        text ="Your email or password is incorrect"
        """Verify that the second 'This field is required' error is visible."""
        assert self.is_visible(self.WRONG_EMAIL_OR_PASSWORD_MESSAGE), "The password required field error message is not visible!"
        self.verify_element_text(self.WRONG_EMAIL_OR_PASSWORD_MESSAGE, UIConstants.INCORRECT_CREDENTIALS)

    def verify_wrong_email(self):
        text ="Your email or password is incorrect"
        """Verify that the second 'This field is required' error is visible."""
        assert self.is_visible(self.WRONG_EMAIL_OR_PASSWORD_MESSAGE), "The password required field error message is not visible!"
        self.verify_element_text(self.WRONG_EMAIL_OR_PASSWORD_MESSAGE, UIConstants.INVALID_EMAIL)


