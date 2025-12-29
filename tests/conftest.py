import json
import os

import allure
import pytest
from appium import webdriver
from appium.options.common import AppiumOptions

from pages.bottom_tabs import BottomTabs
from pages.login_page import LoginPage
from utils.data_provider import DataProvider
from utils.gemini_analyzer import GeminiAnalyzer


@pytest.fixture(scope="function")
def app(driver):
    """Initializes all Page Objects and provides them as a single object."""

    class AppPages:
        def __init__(self, _driver):  # Changed 'driver' to '_driver' to avoid shadowing
            self.login = LoginPage(_driver)
            self.bottom=BottomTabs(_driver)

    return AppPages(driver)

@pytest.fixture(scope="session")
def data():
    """Returns the DataProvider instance to access test data easily."""
    return DataProvider()

def load_config():
    """Reads the configuration from config.json."""
    config_path = os.path.join(os.path.dirname(__file__), "../config/config.json")
    with open(config_path) as f:
        return json.load(f)


def _build_local_capabilities(platform: str, config: dict, base_dir: str) -> dict:
    """Return capabilities for local Android/iOS execution."""
    if platform == "android":
        caps = dict(config["android"])  # copy to avoid mutating loaded config
        caps["app"] = os.path.join(base_dir, caps["app"])
        return caps
    if platform == "ios":
        return dict(config["ios"])
    raise ValueError(f"Platform {platform} is not supported for local run!")


def _build_browserstack_capabilities(config: dict, platform: str) -> tuple[dict, str]:
    """Return (capabilities, remote_url) for BrowserStack execution.

    Uses values under the `browserstack` key in config.json.
    Secrets (user/key) are intentionally placeholders and should be
    overridden via environment variables in real pipelines.
    """
    bs_conf = config.get("browserstack", {})

    user = os.getenv("BROWSERSTACK_USERNAME", bs_conf.get("user", "YOUR_USERNAME"))
    key = os.getenv("BROWSERSTACK_ACCESS_KEY", bs_conf.get("key", "YOUR_ACCESS_KEY"))

    # Generic capabilities for BrowserStack App Automate (Appium)
    bstack_options = {
        "userName": user,
        "accessKey": key,
        "projectName": bs_conf.get("projectName", "Mobile Automation Project"),
        "buildName": bs_conf.get("buildName", "Local Build"),
        "sessionName": bs_conf.get("sessionName", "Sample Test Session"),
        "deviceName": bs_conf.get("deviceName", "Google Pixel 9"),
        "osVersion": bs_conf.get("osVersion", "16.0"),
    }

    caps: dict = {
        "platformName": platform.capitalize(),
        "app": bs_conf.get("app", "bs://YOUR_UPLOADED_APP_ID"),
        "bstack:options": bstack_options,
    }

    remote_url = bs_conf.get("remoteUrl", "http://hub.browserstack.com/wd/hub")
    return caps, remote_url


@pytest.fixture(scope="class")
def driver(request):
    """Setup and teardown for the Appium driver based on platform and environment.

    Examples:
        pytest --platform=android --env=local
        pytest --platform=android --env=browserstack
    """
    platform = request.config.getoption("--platform").lower()
    env = request.config.getoption("--env").lower()

    config = load_config()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    options = AppiumOptions()

    if env == "browserstack":
        caps, remote_url = _build_browserstack_capabilities(config, platform)
    else:
        caps = _build_local_capabilities(platform, config, base_dir)
        remote_url = "http://127.0.0.1:4723"

    options.load_capabilities(caps)

    # Start the session
    driver = webdriver.Remote(remote_url, options=options)

    yield driver

    # Teardown: Close the app after test
    driver.quit()


def pytest_addoption(parser):
    """Custom command line arguments to select platform and execution environment."""
    parser.addoption(
        "--platform",
        action="store",
        default="android",
        help="Platform to run tests: android or ios",
    )
    parser.addoption(
        "--env",
        action="store",
        default="local",
        help="Execution environment: local or browserstack",
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """Attach screenshot and Gemini AI analysis to Allure report on test failure."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed and "driver" in item.fixturenames:
        driver = item.funcargs.get("driver")
        
        # Capture screenshot
        if driver:
            try:
                screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="error_screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception as exc:
                print(f"Failed to capture screenshot for Allure: {exc}")
        
        # Perform Gemini AI analysis
        try:
            analyzer = GeminiAnalyzer()

            # Error message
            error_msg = str(rep.longrepr) if rep.longrepr else "Unknown error"

            # AI analys
            analysis = analyzer.analyze(error_msg[:2000])  # token limit

            # Add yo allure
            allure.attach(
                analysis,
                name="🤖 AI Failure Analysis (Gemini)",
                attachment_type=allure.attachment_type.TEXT,
            )

        except EnvironmentError as e:
            print(f"⚠️ Gemini analysis skipped: {e}")
            allure.attach(
                f"Gemini analysis skipped: {e}\nSet GEMINI_API_KEY environment variable.",
                name="⚠️ AI Analysis Skipped",
                attachment_type=allure.attachment_type.TEXT,
            )
        except Exception as exc:
            print(f"⚠️ Gemini analysis failed: {exc}")
            allure.attach(
                f"Gemini analysis failed: {exc}\nOriginal error: {error_msg}",
                name="⚠️ AI Analysis Error",
                attachment_type=allure.attachment_type.TEXT,
            )

