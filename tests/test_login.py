import allure
import pytest


@allure.feature("Authentication")
class TestSignIn:
    """Tests related to the Sign In flow and Credential Validation."""

    @pytest.fixture(autouse=True)
    def setup_data(self, data, app):
        """
        Setup fixture to prepare user data and navigate to the initial sign-in screen.
        """
        self.valid_user = data.get_user("valid_user")
        self.invalid_user = data.get_user("invalid_user")

        # with allure.step("Navigate to Sign In screen"):
        #     app.login.navigate_to_signin_screen()

    @allure.story("Empty Credentials Validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Verify that 'field required' messages appear when both inputs are empty.")
    def test_required_email_password_fields(self, app):
        with allure.step("Navigate to Sign In screen"):
            app.login.navigate_to_signin_screen()

        with allure.step("Click continue with empty fields"):
            app.login.click(app.login.LOGIN_BUTTON)

        with allure.step("Verify that required error messages are displayed for both fields"):
            app.login.verify_credentials_required_field_visible_1()
            app.login.verify_credentials_required_field_visible_2()

    @allure.story("Invalid Email Format Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Verify the error message when an email is entered without '@' or domain.")
    def test_invalid_email_format(self, app):
        with allure.step(f"Enter malformed email: {self.invalid_user['wrongEmailFormat']}"):
            app.login.type_text(app.login.EMAIL_INPUT, self.invalid_user["wrongEmailFormat"])
        with allure.step("Click on Continue button"):
            app.login.click(app.login.LOGIN_BUTTON)

        with allure.step("Verify 'Invalid Format' error for email and 'Required' error for password"):
            app.login.verify_wrong_email_format_message()
            app.login.verify_required_field_visible()

    @allure.story("Incorrect Credentials - Unregistered Email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_incorrect_email_error_message(self, app):
        with allure.step("Submit login with an unregistered email"):
            app.login.type_text(app.login.EMAIL_INPUT, self.invalid_user["email"])
            app.login.type_text(app.login.PASSWORD_INPUT, self.valid_user["password"])
        with allure.step("Click on Continue button"):
            app.login.click(app.login.LOGIN_BUTTON)

        with allure.step("Verify 'Incorrect Email or Password' system message"):
            app.login.verify_wrong_email()

    @allure.story("Incorrect Credentials - Wrong Password")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_incorrect_password_error_message(self, app):
        with allure.step("Submit login with valid email but wrong password"):
            app.login.type_text(app.login.EMAIL_INPUT, self.valid_user["email"])
            app.login.type_text(app.login.PASSWORD_INPUT, self.invalid_user["password"])
        with allure.step("Click on Continue button"):
            app.login.click(app.login.LOGIN_BUTTON)

        with allure.step("Verify 'Incorrect Email or Password' system message"):
            app.login.verify_wrong_password()

    @allure.story("Password Field Requirement")
    @allure.severity(allure.severity_level.NORMAL)
    def test_required_password_fields(self, app):
        with allure.step("Enter valid email and clear password field"):
            app.login.type_text(app.login.EMAIL_INPUT, self.valid_user["email"])
            app.login.clear_input_field(app.login.PASSWORD_INPUT)
        with allure.step("Click on Continue button"):
            app.login.click(app.login.LOGIN_BUTTON)

        with allure.step("Verify that the password 'Required' message is visible"):
            app.login.verify_required_field_visible()

    @allure.story("Email Field Requirement")
    @allure.severity(allure.severity_level.NORMAL)
    def test_required_email_fields(self, app):
        with allure.step("Enter valid password and clear email field"):
            app.login.type_text(app.login.PASSWORD_INPUT, self.valid_user["password"])
            app.login.clear_input_field(app.login.EMAIL_INPUT)

        with allure.step("Click on Continue button"):
            app.login.click(app.login.LOGIN_BUTTON)

        with allure.step("Verify that the email 'Required' message is visible"):
            app.login.verify_required_field_visible()

    @allure.story("Successful Login with Valid Credentials")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_valid_login(self, app):
        with allure.step(f"Login with credentials: {self.valid_user['email']}"):
            app.login.login(self.valid_user["email"], self.valid_user["password"])

        with allure.step("Verify successful redirection to Home screen (Bottom Tabs visible)"):
            app.bottom.verify_bottom_tabs_visible()