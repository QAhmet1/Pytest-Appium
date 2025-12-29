from __future__ import annotations

import allure


def assert_true(condition, message: str | None = None):
    """Allure-friendly assertion for truthy conditions."""
    text = message or "Expected condition to be True"
    with allure.step(f"Asserting TRUE: {text}"):
        assert condition, text


def assert_equal(expected, actual, message: str | None = None):
    """Allure-friendly equality assertion."""
    text = message or f"Expected '{expected}' but got '{actual}'"
    with allure.step(f"Asserting EQUAL: {text}"):
        assert actual == expected, text


def assert_element_is_displayed(element, message: str | None = None):
    """Assert that a WebElement is displayed and attach a clear message to Allure."""
    text = message or "Expected element to be visible on screen"
    with allure.step(f"Asserting ELEMENT DISPLAYED: {text}"):
        assert element is not None and element.is_displayed(), text

