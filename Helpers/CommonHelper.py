from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from logging import exception


def waitUntilElementVisible(driver, elementLocator, timeout=10):
    element = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(elementLocator))

def waitAndInputText(driver, elementLocator, value):
    retries_left = 2
    while retries_left > 0:
        try:
            element = driver.find_element(*elementLocator)
            element.clear()
            element.send_keys(value)
            return element
        except WebDriverException:
            waitUntilElementVisible(driver, elementLocator, 1)
            retries_left -= 1
    raise exception("Error occurred during text input")


def waitToBeClickable(driver, elementlocator, timeout=3):
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(elementlocator))


def waitAndClick(driver, elementLocator):
    retries_left = 2
    while retries_left > 0:
        try:
            driver.find_element(*elementLocator).click()
            return
        except WebDriverException:
            waitToBeClickable(driver, elementLocator)
            retries_left -= 1
    raise exception("Element is not clickable or not present on page")


def waitAndAssertElementText(driver, elementLocator, value):
    retries_left = 2
    while retries_left > 0:
        try:
            assert(driver.find_element(*elementLocator).text == value)
            return
        except WebDriverException:
            waitToBeClickable(driver, *elementLocator)
            retries_left -= 1

        raise exception("Element is not found or text is not found")

def getElementAttribute(driver, elementLocator, attribute):
    value = driver.find_element(*elementLocator).get_attribute(attribute)
    return value