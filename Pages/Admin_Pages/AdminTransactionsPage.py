from Locators.Admin_Locators.AdminTransactionPageLocators import *
from Pages.BasePage import Page
from selenium.common.exceptions import WebDriverException
import time

class AdminTransactionsPage(Page):
    def find_transaction_by_id(self, transactionid):
        """
        Поиск транзакции по айди
        :param transactionid:
        :return:
        """
        self.wait_and_input_text(AdminTransSearchLocators.transactionID, transactionid)
        self.wait_to_be_clickable(AdminTransSearchLocators.submitButton)
        self.wait_and_click(AdminTransSearchLocators.submitButton)

    def approve_transaction(self):
        """
        апрув транзакции
        :return:
        """
        self.wait_to_be_clickable(AdminTransTableLocators.moreButton)
        self.wait_and_click(AdminTransTableLocators.moreButton)
        self.wait_to_be_clickable(AdminTransTableLocators.approveButton)
        self.wait_and_click(AdminTransTableLocators.approveButton)

    def disapprove_transaction(self):
        """
        дизапрув транзакции
        :return:
        """
        self.wait_to_be_clickable(AdminTransTableLocators.moreButton)
        self.wait_and_click(AdminTransTableLocators.moreButton)
        self.wait_to_be_clickable(AdminTransTableLocators.disapproveButton)
        self.wait_and_click(AdminTransTableLocators.disapproveButton)

    def assert_manual_approve_transaction(self):
        self.wait_and_assert_element_text(AdminTransTableLocators.statusTransaction, "waiting_approval")



