Mobile Automation Framework (Android & iOS)
A professional-grade, cross-platform mobile test automation framework built with Python, Appium, and Pytest. This project demonstrates the implementation of the Page Object Model (POM), scalable test architecture, and advanced reporting.

🚀 Key Features
Cross-Platform Support: Single codebase to run tests on both Android and iOS using dynamic capability switching.

Page Object Model (POM): Enhanced maintainability by separating UI locators from test logic.

Data-Driven Testing: Sensitive information and test data are managed via external JSON configuration files.

Advanced Reporting: Integrated with Allure Reports to provide detailed execution steps, severity levels, and automatic error screenshots.

Robust Synchronization: Custom BasePage methods utilizing WebDriverWait for stable execution against flaky UI elements.

🛠️ Tech Stack
Language: Python 3.10+

Test Runner: Pytest

Mobile Engine: Appium Python Client (targeting Appium 2.x)

Reporting: Allure Pytest

Design Pattern: Page Object Model (POM)

📂 Project Structure
├── config/                 # Environment capabilities and test data (JSON)
├── pages/                  # Page classes (POM) with AppiumBy locators
│   ├── base_page.py        # Common element interactions
│   └── login_page.py       # Login screen specific locators and actions
├── tests/                  # Test suites
│   ├── conftest.py         # Pytest fixtures and driver initialization
│   └── test_login.py       # Functional login tests
├── utilis/                 # Common assertion and helper utilities
├── reports/                # Raw Allure result files
├── run_tests.py            # Short command wrapper to run tests
└── requirements.txt        # Project dependencies

⚙️ Setup & Installation
Clone the repository:

```bash
git clone https://github.com/yourusername/Mobile-Selenium-Appium.git
cd Mobile-Selenium-Appium
```

Create a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configuration: Update `config/config.json` with your specific device details (`deviceName`, `app` path, `platformVersion`).  
For BrowserStack, fill in the `browserstack` section or define `BROWSERSTACK_USERNAME` and `BROWSERSTACK_ACCESS_KEY` as environment variables.

🧪 Running Tests (Short Commands)
- **Android, local Appium server**:

```bash
python run_tests.py --platform android --env local
```

- **iOS, local Appium server**:

```bash
python run_tests.py --platform ios --env local
```

- **Filter by smoke tests**:

```bash
python run_tests.py --platform android --env local -k "smoke"
```

- **(Future) BrowserStack execution** – after you configure credentials:

```bash
python run_tests.py --platform android --env browserstack
```

Under the hood, `run_tests.py` calls `pytest` with the right `--platform` and `--env` flags, and `pytest.ini` is configured to always send Allure results to `./reports`.

📊 Reporting
This framework uses Allure for high-level reporting. To generate and open the report after running tests:

```bash
allure serve ./reports
```

The report includes:

- Step-by-step execution logs.
- Test severity (Critical, Normal, etc.).
- Automatic screenshots attached to failed test cases.