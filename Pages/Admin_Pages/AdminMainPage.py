from Locators.Admin_Locators.AdminMainPageLocators import *
from Pages.BasePage import Page
from selenium.common.exceptions import WebDriverException
import time

class AdminMainPage(Page):
    def go_to_search_transaction(self):
        """
        Переход на страницу списка транзакций
        :return:
        """

        self.wait_and_click(TransactionsSelectors.transDropdown)

        self.wait_and_click(TransactionsSelectors.transList)
