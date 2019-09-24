from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from Locators.DashboardLocators import *
from selenium.webdriver.common.keys import Keys
import time
import conftest
import pytest


class Page(object):
    def __init__(self, driver):
        self.driver = driver
        self.url = conftest.url + '/'


    def get_base_url(self):
        """
        Переходит на стартовую страницу (/auth/login)
        :return:
        """
        self.driver.get(self.url)

    def get_current_url(self):
        """
        Возвращает текущий URL
        :return: string с текущим URL
        """
        return self.driver.current_url

    def wait_to_be_clickable(self, element_locator, timeout=3):
        """
        Поиск и ожидание доступности клика по элементу
        :param element_locator: локатор элемента из Locators/*
        :param timeout: таймаут, по дефолту 3 секунды
        """
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(element_locator))

    def wait_and_input_text(self, element_locator, value):
        """
        Ввод текстовых данных в поле
        :param element_locator: локатор элемента из Locators/*
        :param value: string с данными
        """
        retries_left = 2
        while retries_left > 0:
            try:
                WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(element_locator))
                element = self.driver.find_element(*element_locator)
                element.clear()
                element.send_keys(value)
                return element
            except WebDriverException:
                retries_left -= 1
        raise NoSuchElementException("Error occurred during text input")

    def get_element(self, element_locator, timeout=1):
        try:
            element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(element_locator))
            return True
        except:
            return False


    def wait_until_element_visible(self, element_locator, timeout=3):
        """
        Ожидает пока элемент не станет видимым
        :param element_locator: локатор элемента из Locators/*
        :param timeout: таймаут, по умолчанию 3 секунды
        """
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(element_locator))

    def wait_until_element_invisible(self, element_locator, timeout=0):
        """
        Проверяет что элемент не виден на странице
        :param element_locator: локатор элемента из Locators/*
        :param timeout: таймаут, по умолчанию 0 секунд
        :return:
        """
        element = WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(element_locator))


    def wait_and_click(self, element_locator):
        """
        Ожидает элемент и кликает по нему
        :param element_locator: локатор элемента из Locators/*
        """
        retries_left = 2
        while retries_left > 0:
            try:
                WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(element_locator))
                self.driver.find_element(*element_locator).click()
                return
            except (WebDriverException, TimeoutError) as e:
                retries_left -= 1
        raise NoSuchElementException("Element is not clickable or not present on page")

    def assert_element_text(self, element_locator, value, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(element_locator, value))


    def wait_and_assert_element_text(self, element_locator, value):
        """
        Ожидает элемент и сравнивает его текст со значением
        :param element_locator: локатор элемента из Locators/*
        :param value: Значение с которым сравнивается текст элемента
        """
        retries_left = 3
        while retries_left > 0:
            try:
                WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(element_locator))
                text = self.driver.find_element(*element_locator).text
                assert (text == value)
                return
            except (AssertionError, WebDriverException) as e:
                self.wait_until_element_visible(element_locator)
                retries_left -= 1
                time.sleep(2)
        raise NoSuchElementException("Element is not found or text is not found")

    def get_element_attribute(self, element_locator, attribute):
        """
        Возвращает значение атрибута элемента
        :param element_locator: локатор элемента из Locators/*
        :param attribute: название атрибута ("disabled", "text()")
        :return: значение атрибута (string, boolean или None)
        """
        value = self.driver.find_element(*element_locator).get_attribute(attribute)
        return value

    def get_element_text(self, element_locator):
        """
        Возвращает значение атрибута элемента
        :param element_locator: локатор элемента из Locators/*
        :return: текст элемента
        """
        retries_left = 3
        while retries_left > 0:
            try:
                WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(element_locator))
                text = self.driver.find_element(*element_locator).text
                return text
            except (AssertionError, WebDriverException) as e:
                retries_left -= 1
        raise NoSuchElementException("Element is not found or text is not found")

    def hover_over_element(self, element_locator):
        retries_left = 2
        while retries_left > 0:
            try:
                element = self.driver.find_element(*element_locator)
                action = ActionChains(self.driver)
                hover = action.move_to_element(element)
                hover.perform()
                return
            except (AssertionError, WebDriverException) as e:
                retries_left -= 1
                time.sleep(1)
        raise NoSuchElementException("Element is not found or text is empty")

    def hover_and_click(self, element_locator):

        element = self.driver.find_element(*element_locator)
        action = ActionChains(self.driver)
        click = action.move_to_element_with_offset(element, -50, -50).click().perform()

    def send_escape(self):
        action = ActionChains(self.driver)
        action.send_keys(Keys.ESCAPE).perform()

    def close_alert(self):
        alert = self.driver.switch_to.alert
        alert.accept()


    def assert_element_text_is_not_empty(self, element_locator):
        """
        Проверка того что в элементе есть какой-либо текст и он не пустая строка
        :param element_locator: локатор элемента из Locators/*
        """
        retries_left = 2
        while retries_left > 0:
            try:
                WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(element_locator))
                assert (self.driver.find_element(*element_locator).text is not None or '')
                return
            except (AssertionError, WebDriverException) as e:
                self.wait_until_element_visible(element_locator)
                retries_left -= 1
        raise ValueError("Element is not found or text is empty")

    def assert_element_text_is_not_equal(self, element_locator, value):
        """
        Проверка что текст в элементе НЕ равен значению
        :param element_locator: локатор элемента из Locators/*
        :param value: значение которому должен быть НЕ равен текст в элементе
        """
        retries_left = 2
        while retries_left > 0:
            try:
                WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(element_locator))
                assert (self.driver.find_element(*element_locator).text != value)
                return
            except (AssertionError, WebDriverException) as e:
                retries_left -= 1
        raise ValueError("Element is not found or text equal to value")

    def navigate_to_link(self, link):
        """
        Переход по ссылке со страницы и возвращение на эту страницу
        Используется для всяких verification link из писем
        :param link: ссылка по которой надо перейти
        """
        print(link)
        current_url = self.driver.current_url
        self.driver.get(link)
        self.driver.get(self.url)

    def reset_session(self):
        """
        Чистит текущую сессию и возвращается к начальной странице
        :return:
        """
        self.driver.execute_script("window.localStorage.clear();")
        self.driver.execute_script("window.sessionStorage.clear();")
        time.sleep(0.5)
        self.get_base_url()
        time.sleep(0.5)

        retries_left = 4
        while retries_left > 0:
            if not (self.driver.current_url == self.url or self.driver.current_url == ("%sauth/login" % self.url)):
                self.driver.execute_script("window.localStorage.clear();")
                self.driver.execute_script("window.sessionStorage.clear();")
                time.sleep(0.5)
                self.get_base_url()
                time.sleep(0.5)
                retries_left -= 1
            else:
                return

    def refresh_page(self):
        """
        Перезагружает текущую страницу (учитывайте что после нужно вводить пин-код)
        """
        self.driver.refresh()

    def assert_element_attirbute_value(self, element_locator, attribute, value):
        """
        Сравнивает значение атрибута элемента с заданным значением
        :param element_locator: локатор элемента из Locators/*
        :param attribute: название атрибута
        :param value: значение, с которым сравнивается значение атрибута
        """
        attribute_value = self.get_element_attribute(element_locator, attribute)
        assert attribute_value == value


    def wait_and_click_element_within_element(self, node_locator, element_locator):
        """
        Находит элемент внутри другого элемента и кликает по нему
        :param node_locator: локатор родительского элемента из Locators/*
        :param element_locator: локатор дочернего элемента из Locators/*
        """
        retries_left = 2
        while retries_left > 0:
            try:
                node_element = self.driver.find_element(*node_locator)
                node_element.find_element(*element_locator).click()
                return
            except WebDriverException:
                self.wait_to_be_clickable(element_locator)
                time.sleep(0.5)
                retries_left -= 1
        raise WebDriverException("Element is not clickable or not present on page")


    def navigate_to_dashboard(self):
        self.wait_to_be_clickable(NavigationButtons.dashboard)
        self.wait_and_click(NavigationButtons.dashboard)

    def move_mouse_in_element(self, element_locator):
        element = self.driver.find_element(*element_locator)
        action = ActionChains(self.driver)
        move = action.move_to_element_with_offset(element, 150, 150).perform()

