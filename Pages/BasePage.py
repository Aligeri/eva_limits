from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from Locators.DashboardLocators import *
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
import conftest
import pytest


class Page(object):

    admin_url = "https://board.cain.loc/"

    def __init__(self, driver):
        self.driver = driver
        self.url = conftest.url + '/'

    def get_html(self):
        html = self.driver.page_source
        return html

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

    def wait_to_be_clickable(self, element_locator, timeout=5):
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
                WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(element_locator))
                element = self.driver.find_element(*element_locator)
                element.clear()
                element.send_keys(value)
                return element
            except WebDriverException:
                retries_left -= 1
        raise NoSuchElementException("Error occurred during text input")

    def upload_file(self, element_locator, file_path):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(element_locator))
        element = self.driver.find_element(*element_locator)
        element.send_keys(file_path)

    def clear_field(self, element_locator):
        element = self.driver.find_element(*element_locator)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().click().send_keys(Keys.DELETE).perform()

    def get_element(self, element_locator, timeout=1):
        try:
            element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(element_locator))
            return True
        except:
            return False


    def wait_until_element_visible(self, element_locator, timeout=3, polling=0.5):
        """
        Ожидает пока элемент не станет видимым
        :param element_locator: локатор элемента из Locators/*
        :param timeout: таймаут, по умолчанию 3 секунды
        """
        element = WebDriverWait(self.driver, timeout, polling).until(
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
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(element_locator))
                self.driver.find_element(*element_locator).click()
                return
            except (WebDriverException, TimeoutError) as e:
                time.sleep(0.5)
                retries_left -= 1
        raise NoSuchElementException("Element is not clickable or not present on page: " + str(element_locator))

    def assert_element_text(self, element_locator, value, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(element_locator, value))

    def assert_element_text_contains_value(self, element_locator, value):
        text = self.get_element_text(element_locator)
        assert value in text\

    def assert_element_text_not_contains_value(self, element_locator, value):
        text = self.get_element_text(element_locator)
        assert value not in text


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

    def send_enter(self):
        action = ActionChains(self.driver)
        action.send_keys(Keys.ENTER).perform()

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
        self.driver.execute_script("indexedDB.deleteDatabase('firebaseLocalStorageDb')")
        self.driver.execute_script('indexedDB.deleteDatabase("redux-persist-fw")')
        self.get_base_url()

        retries_left = 4
        while retries_left > 0:
            time.sleep(0.5)
            try:
                if (self.driver.current_url == ("%sauth/pin-check" % self.url)):
                    cancel = self.driver.find_element(By.XPATH,
                                                      "//div[contains(@class, 'auth__authCodeActions--3iRx1 auth__formActions--17Eei')]")
                    cancel.click()
            except:
                pass
            if not (self.driver.current_url == self.url or self.driver.current_url == ("%sauth/login" % self.url)):
                self.driver.execute_script("window.localStorage.clear();")
                self.driver.execute_script("window.sessionStorage.clear();")
                self.driver.execute_script("indexedDB.deleteDatabase('firebaseLocalStorageDb')")
                self.driver.execute_script('indexedDB.deleteDatabase("redux-persist-fw")')
                self.get_base_url()
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

    def find_element_within_element(self, node_locator, element_locator):
        """
        Находит элемент внутри другого элемента
        :param node_locator: локатор родительского элемента из Locators/*
        :param element_locator: локатор дочернего элемента из Locators/*
        :return: дочерний элемент внутри родительского элемента
        """
        retries_left = 2
        while retries_left > 0:
            try:
                node_element = self.driver.find_element(*node_locator)
                child_element = node_element.find_element(*element_locator)
                return child_element
            except WebDriverException:
                time.sleep(0.5)
                retries_left -= 1
        raise WebDriverException("Element is not present on page")

    def get_element_text_within_element(self, node_locator, element_locator):
        """
        Находит элемент внутри другого элемента
        :param node_locator: локатор родительского элемента из Locators/*
        :param element_locator: локатор дочернего элемента из Locators/*
        :return: дочерний элемент внутри родительского элемента
        """
        retries_left = 2
        while retries_left > 0:
            try:
                node_element = self.driver.find_element(*node_locator)
                child_element_text = node_element.find_element(*element_locator).text
                return child_element_text
            except WebDriverException:
                time.sleep(0.5)
                retries_left -= 1
        raise WebDriverException("Element is not present on page")

    def get_element_text_within_webelement(self, node_webelement, element_locator):
        """
        Находит элемент внутри другого элемента
        :param node_webelement: родительский элемент (!! не локатор !!)
        :param element_locator: локатор дочернего элемента из Locators/*
        :return: дочерний элемент внутри родительского элемента
        """
        retries_left = 2
        while retries_left > 0:
            try:
                child_element_text = node_webelement.find_element(*element_locator).text
                return child_element_text
            except WebDriverException:
                time.sleep(0.5)
                retries_left -= 1
        raise WebDriverException("Element is not present on page")

    def get_text_from_webelement(self, webelement):
        text = webelement.text
        return text


    def navigate_to_dashboard(self):
        self.wait_to_be_clickable(NavigationButtons.dashboard)
        self.wait_and_click(NavigationButtons.dashboard)

    def move_mouse_in_element(self, element_locator):
        element = self.driver.find_element(*element_locator)
        action = ActionChains(self.driver)
        move = action.move_to_element_with_offset(element, 150, 150).perform()

    def get_current_time(self):
        DT_FORMAT = '%Y-%m-%d %H:%M:%S'
        now = datetime.utcnow()
        return now.strftime(DT_FORMAT)
    def get_elements_count(self, element_locator):
        elements = self.driver.find_elements(*element_locator)
        count = len(elements)
        return count

    def get_elements(self, element_locator):
        retries_left = 2
        while retries_left > 0:
            try:
                elements = self.driver.find_elements(*element_locator)
                return elements
            except WebDriverException:
                self.wait_until_element_visible(element_locator)
                retries_left -= 1
        raise WebDriverException("Elements are not present on page")



    def clear_input_text(self, element_locator):
        """
        Очищает поле в инпуте, если он с автозаполнением и не работает стадартный clear()
        """
        retries_left = 2
        while retries_left > 0:
            try:
                WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(element_locator))
                element = self.driver.find_element(*element_locator)
                element.click()
                for i in range(len(element.get_attribute('value'))):
                    element.send_keys(Keys.BACK_SPACE)
                return
            except WebDriverException:
                retries_left -= 1
        raise NoSuchElementException("Error occurred during clear input")

    def find_element_within_webelement(self, parent_element, child_locator):
        """
        Находит элемент внутри другого элемента
        :param parent_element: родительский веб элемент (не локатор)
        :param child_locator: локатор дочернего элемента из Locators/*
        :return: дочерний элемент внутри родительского элемента
        """
        retries_left = 2
        while retries_left > 0:
            try:
                child_element = parent_element.find_element(*child_locator)
                return child_element
            except WebDriverException:
                time.sleep(0.5)
                retries_left -= 1
        raise WebDriverException("Element is not present on page")

    def wait_and_click_element_within_webelement(self, parent_element, child_locator):
        """
        Находит элемент внутри другого вебэлемента и кликает по нему
        :param parent_element: родительский веб элемент (не локатор)
        :param child_locator: локатор дочернего элемента из Locators/*
        """
        retries_left = 2
        while retries_left > 0:
            try:
                text = self.get_text_from_webelement(parent_element)
                self.find_element_within_webelement(parent_element, child_locator).click()
                return
            except WebDriverException:
                self.wait_to_be_clickable(child_locator)
                time.sleep(0.5)
                retries_left -= 1
        raise WebDriverException("Element is not clickable or not present on page")