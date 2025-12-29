import os
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions


class GeminiAnalyzer:
    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            print("WARNING: API Key not found, analysis will not run.")
            self.model = None
            return

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("models/gemini-2.5-flash")

    def analyze(self, error_log: str) -> str:
        if not self.model:
            return "Gemini API Key is missing, analysis cannot be performed."

        prompt = f"""
        You are a senior QA automation engineer.
        Analyze the following Python/Appium test failure.

        1. Clearly explain WHY the assertion failed based on the logs.
        2. Suggest a potential fix for the code or the test data.

        Error Log:
        {error_log}
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()

        except google_exceptions.NotFound:
            return "Error: The specified model was not found. Check the model name (e.g., models/gemini-2.5-flash)."
        except Exception as e:
            return f"An unexpected error occurred during Gemini analysis: {str(e)}"
