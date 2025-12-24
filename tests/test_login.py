
import allure
import pytest

@allure.feature("Authentication")
class TestSignIn:
    """Tests related to the Sign In flow."""

    @pytest.fixture(autouse=True)
    def setup_data(self, data):
        """
        This fixture runs automatically before each test in this class.
        It sets up the 'valid_user' data once.
        """
        self.valid_user = data.get_user("valid_user")
        self.invalid_user=data.get_user("invalid_user")

    @allure.story("Verify required error messages fields")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_required_email_password_fields(self, app):
        with allure.step("Leave credentials empty, click login, and verify required error messages"):
            with allure.step("Navigate to signin screen"):
                app.login.navigate_to_signin_screen()
            with allure.step("Click on Continue button"):
              app.login.click(app.login.LOGIN_BUTTON)
            with allure.step("Verify the required error messages displayed "):
              app.login.verify_credentials_required_field_visible_1()
              app.login.verify_credentials_required_field_visible_2()

    @allure.story("Verify invalid email format message")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_invalid_email_format(self, app):
        with allure.step("Enter wrong format email, keep password empty and click continue button"):
            with allure.step("Enter wrong email format"):
                app.login.type_text(app.login.EMAIL_INPUT,"wrongemailformat%")
            with allure.step("Click on Continue button"):
                app.login.click(app.login.LOGIN_BUTTON)
            with allure.step("Verify the wrong format error message displayed "):
                app.login.verify_wrong_email_format_message()
            with allure.step("Verify the required field message displayed for password "):
                app.login.verify_required_field_visible()

    @allure.story("Verify incorrect email error message")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_incorrect_email_error_message(self, app):
        with allure.step("Enter invalid email, enter valid password, click continue button and check error message"):
            with allure.step("Enter invalid email"):
                app.login.type_text(app.login.EMAIL_INPUT,self.invalid_user["email"])
            with allure.step("Enter invalid email"):
                app.login.type_text(app.login.PASSWORD_INPUT,self.valid_user["password"])
            with allure.step("Click on Continue button"):
                app.login.click(app.login.LOGIN_BUTTON)
            with allure.step("Verify the wrong credentials message appears"):
                app.login.verify_wrong_email()

    @allure.story("Verify incorrect password error message")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_incorrect_password_error_message(self, app):
        with allure.step("Enter valid email, enter invalid password, click continue button and check error message"):
            with allure.step("Enter invalid email"):
                app.login.type_text(app.login.EMAIL_INPUT,self.valid_user["email"])
            with allure.step("Enter invalid email"):
                app.login.type_text(app.login.PASSWORD_INPUT,self.invalid_user["password"])
            with allure.step("Click on Continue button"):
                app.login.click(app.login.LOGIN_BUTTON)
            with allure.step("Verify the wrong credentials message appears"):
                app.login.verify_wrong_password()

    @allure.story("Verify required error messages for password field")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_required_password_fields(self, app):
        with allure.step("Enter email, keep password is empty, click login, and verify required error message for password"):
            app.login.type_text(app.login.EMAIL_INPUT,self.valid_user["email"])
            app.login.clear_input_field(app.login.PASSWORD_INPUT)
            app.login.click(app.login.LOGIN_BUTTON)

        with allure.step("Verify the 'This field is required' message is visible"):
            app.login.verify_required_field_visible()

    @allure.story("Verify required error messages for email field")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_required_email_fields(self, app):
        with allure.step("Enter password, keep email is empty, click login, and verify required error message for email"):
            with allure.step("Enter password"):
              app.login.type_text(app.login.PASSWORD_INPUT, self.valid_user["password"])
            with allure.step("Clean email input"):
              app.login.clear_input_field(app.login.EMAIL_INPUT)
            with allure.step("Click on continue button"):
              app.login.click(app.login.LOGIN_BUTTON)
            with allure.step("Verify the 'This field is required' message is visible"):
              app.login.verify_required_field_visible()

    @allure.story("Verify Valid Email and Password")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_valid_login(self, app):

        # Step 1: Perform Login
        with allure.step(f"Enter credentials for {self.valid_user['email']} and click login"):
            app.login.login(self.valid_user["email"], self.valid_user["password"])

        # Step 2: Verify user logged in
        with allure.step("Verify bottom tabs elements are visible"):
            app.bottom.verify_bottom_tabs_visible()
