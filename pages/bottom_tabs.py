
from appium.webdriver.common.appiumby import AppiumBy  # Correct import for Appium locators
from pages.base_page import BasePage

class BottomTabs(BasePage):
   HOME= (AppiumBy.XPATH,"//android.widget.TextView[@text='Home']")
   PORTFOLIO= (AppiumBy.XPATH,"//android.widget.TextView[@text='Portfolio']")
   MARKETS= (AppiumBy.XPATH,"//android.widget.TextView[@text='Markets']")
   MORE= (AppiumBy.XPATH,"//android.widget.TextView[@text='More']")

   def verify_bottom_tabs_visible(self):
       """Tüm alt tabların görünür olduğunu doğrular."""
       tabs = [self.HOME, self.PORTFOLIO, self.MARKETS, self.MORE]
       for tab in tabs:
           # is_visible provides built-in waiting logic (Explicit Wait)
           is_tab_displayed = self.is_visible(tab, timeout=7)

           # If is_visible returns False, the assertion will fail with a clear message
           assert is_tab_displayed is True, f"Navigation failure: '{tab}' tab is not visible."

