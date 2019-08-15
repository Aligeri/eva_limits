from Pages.BasePage import Page
from Locators.DashboardLocators import *
from Locators.WalletLocators import *


class DashboardPage(Page):
    def select_language(self, language):
        pass

    def navigate_to_receive(self):
        self.wait_and_click(WalletActionsButtons.receive)

    def select_wallet(self, wallet):
        """
        Выбор кошелька в receive
        :param wallet: валюта кошелька, Ardor/Bitcoin/Bitcoin Cash
        """
        WALLET = {
            "Ardor": ReceiveWallets.ardr,
            "Bitcoin": ReceiveWallets.btc,
            "Bitcoin Cash": ReceiveWallets.bcc,
        }
        self.wait_and_click(WALLET[wallet])

    def assert_deposit_address_is_not_empty(self):
        """
        Проверяет что deposit_address у кошелька не пустой
        """
        self.assert_element_text_is_not_empty(DepositAddress.currentAddress)

    def get_current_deposit_address(self):
        """
        Получает текущий deposit address выбранного кошелька
        :return: возвращает string с deposit address
        """
        return self.get_element_attribute(DepositAddress.currentAddress, "text()")

    def generate_new_deposit_address(self, current_address):
        """
        Генерирует новый deposit address у текущего выбранного кошелька
        Проверяет что новый deposit address не равен старому
        :param current_address: старый deposit address
        """
        self.wait_and_click(DepositAddress.generateNew)
        self.assert_element_text_is_not_equal(DepositAddress.currentAddress, current_address)

    def check_previous_address_in_list(self, current_address):
        """
        Проверяет наличие старого deposit address в списке предыдущих адресов на втором месте в листе
        :param current_address: старый deposit address
        """
        self.wait_and_click(DepositAddress.showAll)
        previous_address = self.get_element_attribute(DepositAddress.previousAddress2, "text()")
        assert previous_address == current_address
