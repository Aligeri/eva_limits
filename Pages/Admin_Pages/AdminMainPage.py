from Locators.Admin_Locators.AdminMainPageLocators import *
from Pages.BasePage import Page
from selenium.common.exceptions import WebDriverException
import time

class AdminMainPage(Page):
    def login_as_admin_user(self, username, password):
        """
        Авторизация в админке
        :param username: емейл с доступом в админку
        :param password:
        :return:
        """
        self.wait_and_input_text(AdminLoginPageLocators.emailField, username)
        self.wait_and_input_text(AdminLoginPageLocators.passwordField, password)
        self.wait_to_be_clickable(AdminLoginPageLocators.signInButton)
        self.wait_and_click(AdminLoginPageLocators.signInButton)

    def go_to_search_transaction(self):
        """
        Переход на страницу списка транзакций
        :return:
        """

        self.wait_and_click(TransactionsSelectors.transDropdown)

        self.wait_and_click(TransactionsSelectors.transList)
