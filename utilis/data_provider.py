import json
import os

class DataProvider:
    def __init__(self):
        # Path to your test_data.json
        self.path = os.path.join(os.path.dirname(__file__), "../config/test_data.json")
        with open(self.path) as f:
            self._data = json.load(f)

    def get_user(self, user_key: str) -> dict:
        """Returns the full dictionary for a specific user (email and password)."""
        return self._data.get(user_key, {})

    def get_email(self, user_key: str) -> str:
        """Returns only the email address for a specific user."""
        return self._data.get(user_key, {}).get("email", "")

    def get_password(self, user_key: str) -> str:
        """Returns only the password for a specific user."""
        return self._data.get(user_key, {}).get("password", "")