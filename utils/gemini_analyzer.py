import os
import warnings

# Suppress FutureWarning from deprecated google.generativeai package at import time
warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    message="All support for the `google.generativeai` package has ended.*",
)

import google.genai as genai
from google.api_core import exceptions as google_exceptions


class GeminiAnalyzer:
    """
    Lightweight Gemini failure analyzer.

    This is not critical for test pass/fail, so:
    - If API key is missing, tests will NOT fail; a message is returned instead.
    - Model / SDK warnings are kept to a minimum.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            # Disable AI analysis silently without breaking test flow
            self.model = None
            return

        # Suppress local FutureWarning from the deprecated generativeai package
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=FutureWarning)
            genai.configure(api_key=api_key)
            # Stabil, text destekleyen bir model kullan
            self.model = genai.GenerativeModel("models/gemini-2.0-flash-exp")

    def analyze(self, error_log: str) -> str:
        """Return human-readable analysis, or a short info message."""
        if not self.model:
            return "Gemini API Key is missing, AI analysis is skipped."

        prompt = f"""
You are a senior QA automation engineer.
Analyze the following Python/Appium test failure log and answer in clear, concise English.

1. Short summary of the failure.
2. Most probable root cause.
3. Is the issue in the test code, the app, or the environment? (with justification).
4. Step-by-step fix recommendations.

Error log:
{error_log}
"""

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=FutureWarning)
                response = self.model.generate_content(prompt)
            return (response.text or "").strip()

        except google_exceptions.NotFound:
            return (
                "Gemini AI analysis skipped: model not found. "
                "Check model name / API access."
            )
        except Exception as e:
            return f"Gemini AI analysis skipped due to error: {str(e)}"
