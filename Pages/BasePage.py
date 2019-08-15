from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from logging import exception
import time
import pytest


class Page(object):
    def __init__(self, driver):
        self.driver = driver
        #self.url = url

    def get_current_url(self):
        return self.driver.current_url()

    def wait_to_be_clickable(self, elementlocator, timeout=3):
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(elementlocator))

    def wait_and_input_text(self, elementLocator, value):
        retries_left = 2
        while retries_left > 0:
            try:
                element = self.driver.find_element(*elementLocator)
                element.clear()
                element.send_keys(value)
                return element
            except WebDriverException:
                self.wait_until_element_visible(elementLocator, 1)
                retries_left -= 1
        raise WebDriverException("Error occurred during text input")

    def wait_until_element_visible(self, elementLocator, timeout=3):
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(elementLocator))

    def wait_and_click(self, elementLocator):
        retries_left = 2
        while retries_left > 0:
            try:
                self.driver.find_element(*elementLocator).click()
                return
            except WebDriverException:
                self.wait_to_be_clickable(elementLocator)
                retries_left -= 1
        raise WebDriverException("Element is not clickable or not present on page")

    def wait_and_assert_element_text(self, elementLocator, value):
        retries_left = 2
        while retries_left > 0:
            try:
                text = self.driver.find_element(*elementLocator).text
                assert (text == value)
                return
            except (AssertionError, WebDriverException) as e:
                self.wait_until_element_visible(elementLocator)
                retries_left -= 1
                time.sleep(2)
        raise WebDriverException("Element is not found or text is not found")

    def get_element_attribute(self, elementLocator, attribute):
        value = self.driver.find_element(*elementLocator).get_attribute(attribute)
        return value

    def assert_element_text_is_not_empty(self, elementLocator):
        retries_left = 2
        while retries_left > 0:
            try:
                assert (self.driver.find_element(*elementLocator).text is not None or '')
                return
            except (AssertionError, WebDriverException) as e:
                self.wait_until_element_visible(elementLocator)
                retries_left -= 1
                time.sleep(1)
        raise WebDriverException("Element is not found or text is empty")

    def assert_element_text_is_not_equal(self, elementLocator, value):
        retries_left = 2
        while retries_left > 0:
            try:
                assert (self.driver.find_element(*elementLocator).text != value)
                return
            except (AssertionError, WebDriverException) as e:
                self.wait_until_element_visible(elementLocator)
                retries_left -= 1
                time.sleep(1)
        raise WebDriverException("Element is not found or text equal to value")

    def navigate_to_link(self, link):
        print(link)
        currentUrl = self.driver.current_url
        self.driver.get(link)
        self.driver.get(currentUrl)

    def refresh_page(self):
        self.driver.refresh()
