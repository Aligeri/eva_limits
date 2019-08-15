from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import time


class Page(object):
    def __init__(self, driver):
        self.driver = driver
        # self.url = url

    def get_current_url(self):
        return self.driver.current_url()

    def wait_to_be_clickable(self, element_locator, timeout=3):
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(element_locator))

    def wait_and_input_text(self, element_locator, value):
        retries_left = 2
        while retries_left > 0:
            try:
                element = self.driver.find_element(*element_locator)
                element.clear()
                element.send_keys(value)
                return element
            except WebDriverException:
                self.wait_until_element_visible(element_locator, 1)
                retries_left -= 1
        raise WebDriverException("Error occurred during text input")

    def wait_until_element_visible(self, element_locator, timeout=3):
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(element_locator))

    def wait_and_click(self, element_locator):
        retries_left = 2
        while retries_left > 0:
            try:
                self.driver.find_element(*element_locator).click()
                return
            except WebDriverException:
                self.wait_to_be_clickable(element_locator)
                retries_left -= 1
        raise WebDriverException("Element is not clickable or not present on page")

    def wait_and_assert_element_text(self, element_locator, value):
        retries_left = 2
        while retries_left > 0:
            try:
                text = self.driver.find_element(*element_locator).text
                assert (text == value)
                return
            except (AssertionError, WebDriverException) as e:
                self.wait_until_element_visible(element_locator)
                retries_left -= 1
                time.sleep(2)
        raise WebDriverException("Element is not found or text is not found")

    def get_element_attribute(self, element_locator, attribute):
        value = self.driver.find_element(*element_locator).get_attribute(attribute)
        return value

    def assert_element_text_is_not_empty(self, element_locator):
        retries_left = 2
        while retries_left > 0:
            try:
                assert (self.driver.find_element(*element_locator).text is not None or '')
                return
            except (AssertionError, WebDriverException) as e:
                self.wait_until_element_visible(element_locator)
                retries_left -= 1
                time.sleep(1)
        raise WebDriverException("Element is not found or text is empty")

    def assert_element_text_is_not_equal(self, element_locator, value):
        retries_left = 2
        while retries_left > 0:
            try:
                assert (self.driver.find_element(*element_locator).text != value)
                return
            except (AssertionError, WebDriverException) as e:
                self.wait_until_element_visible(element_locator)
                retries_left -= 1
                time.sleep(1)
        raise WebDriverException("Element is not found or text equal to value")

    def navigate_to_link(self, link):
        print(link)
        current_url = self.driver.current_url
        self.driver.get(link)
        self.driver.get(current_url)

    def refresh_page(self):
        self.driver.refresh()
