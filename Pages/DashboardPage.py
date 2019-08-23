from Pages.BasePage import Page
from Locators.DashboardLocators import *
from Locators.WalletLocators import *
import re

FILTER_APPLY = {
    "Exchange": Filters.exchangeFilter,
    "Pay Out": Filters.payOutFilter,
    "Pay In": Filters.payInFilter,
    "Failed": Filters.failedFilter,
}
FILTER_BUTTON = {
    "Exchange": Filters.exchangeButton,
    "Pay Out": Filters.payOutButton,
    "Pay In": Filters.payInButton,
    "Failed": Filters.failedButton,
}

class DashboardPage(Page):
    def select_language(self, language):
        pass

    def navigate_to_receive(self):
        self.wait_and_click(WalletActionsButtons.receive)

    def navigate_to_send(self):
        self.wait_and_click(WalletActionsButtons.send)

    def navigate_to_history(self):
        self.wait_and_click(WalletActionsButtons.history)

    def navigate_to_dashboard(self):
        self.wait_and_click(NavigationButtons.dashboard)

    def navigate_to_settings(self):
        self.wait_and_click(NavigationButtons.settings)

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

    def checkFiatSymbols(self, fiat_symbol):
        """
        Проверяет символ текущей фиатной валюты пользователя в total balance, my wallets, графике и в send
        :param fiat_symbol: символ фиатной валюты, $/€
        """
        self.navigate_to_history()
        assert re.search("(\W)\d", self.get_element_text(Fiat.totalFiat)).group(1) == fiat_symbol
        assert re.search("(\W)\d", self.get_element_text(Fiat.walletsFiat)).group(1) == fiat_symbol
        self.wait_and_click(WalletActionsButtons.firstWallet)
        assert re.search("(\W)\d", self.get_element_text(Fiat.graphFiat)).group(1) == fiat_symbol
        self.navigate_to_send()
        assert re.search("(\W)\d", self.get_element_text(Fiat.sendFiat)).group(1) == fiat_symbol

    def apply_filter(self, history_filter):
        """
        Применяет фильтры на странице History
        :param history_filter: название фильтра, Exchange, Pay Out, Pay In, Failed
        """
        self.wait_and_click(Filters.filtersButton)
        self.wait_and_click(FILTER_APPLY[history_filter])
        self.wait_and_click(Filters.applyFilters)
        self.wait_until_element_visible(FILTER_BUTTON[history_filter])

    def remove_filter(self, history_filter):
        """
        Отключает фильтры на странице History
        :param history_filter: название фильтра, Exchange, Pay Out, Pay In, Failed
        """
        self.wait_and_click_element_within_element(FILTER_BUTTON[history_filter], Filters.removeFilter)
        self.wait_until_element_invisible(FILTER_BUTTON[history_filter], 0.5)