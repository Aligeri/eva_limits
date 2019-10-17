from Pages.BasePage import Page
from Locators.DashboardLocators import *
from Locators.WalletLocators import *
import re
import time

LANGUAGE = {
    "en": LanguageSelectors.en,
    "ja": LanguageSelectors.ja,
    "ko": LanguageSelectors.ko,
}

BUY_CURRENCY = {
    "BTC": BuyWithACard.bitcoin,
    "ETH": BuyWithACard.ethereum,
    "LTC": BuyWithACard.litecoin,
}

GRAPH_PERIOD = {
    "day": Graph.day,
    "week": Graph.week,
    "month": Graph.month,
}

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
        #self.hover_over_element(LanguageSelectors.dropdown)
        self.wait_and_click(LanguageSelectors.dropdown)
        self.wait_and_click(LANGUAGE[language])

    def navigate_to_receive(self):
        self.wait_and_click(WalletActionsButtons.receive)

    def check_receive_wallet(self, currency, extra_id=False):
        self.select_wallet(currency)
        self.wait_until_element_visible(DepositAddress.depositAddress)
        assert self.get_element_text(DepositAddress.depositAddress) is not None
        assert self.get_element_text(DepositAddress.userId) is not None
        assert self.get_element_text(DepositAddress.link) is not None
        if extra_id:
            assert self.get_element_text(DepositAddress.memo) is not None
        self.select_wallet(currency)
        time.sleep(0.5)

    def check_top_up_wallet(self, currency, minimum=False):
        self.select_top_up_wallet(currency)
        assert self.get_element_text(TopUpWallets.depositAddress) is not None
        if minimum:
            self.wait_until_element_visible(DepositAddress.minimumBlock)
            amount = self.get_element_text(DepositAddress.minimumAmount)
            list = amount.split(" ")
            assert list[0] is not None
            assert list[0] != "NaN"
        self.select_top_up_wallet(currency)
        time.sleep(0.5)

    def navigate_to_send(self):
        self.wait_and_click(WalletActionsButtons.send)

    def navigate_to_history(self):
        self.wait_and_click(WalletActionsButtons.history)

    def navigate_to_settings(self):
        self.wait_and_click(NavigationButtons.settings)

    def navigate_to_buy_with_a_card(self):
        self.wait_and_click(WalletActionsButtons.buy)
        
    def select_wallet(self, wallet):
        """
        Выбор кошелька в receive
        :param wallet: валюта кошелька, Ardor/Bitcoin/Bitcoin Cash
        """
        WALLET = {
            "Ardor": ReceiveWallets.ardr,
            "Bitcoin": ReceiveWallets.btc,
            "Bitcoin Cash": ReceiveWallets.bcc,
            "Dogecoin": ReceiveWallets.doge,
            "Ethereum": ReceiveWallets.eth,
            "EOS": ReceiveWallets.eos
        }
        self.wait_and_click(WALLET[wallet])

    def select_top_up_wallet(self, wallet):
        """
        Выбор кошелька в receive
        :param wallet: валюта кошелька, Ardor/Bitcoin/Bitcoin Cash
        """
        WALLET = {
            "Ardor": TopUpWallets.ardr,
            "Bitcoin": TopUpWallets.btc,
            "Bitcoin Cash": TopUpWallets.bcc,
            "Ethereum": TopUpWallets.eth,
            "Doge": TopUpWallets.doge,
            "EOS": TopUpWallets.eos
        }
        self.wait_and_click(WALLET[wallet])

    def select_buy_currency(self, currency):
        self.wait_and_click(BUY_CURRENCY[currency])
        buy_text = "Buy %s" % currency
        self.wait_to_be_clickable(BuyWithACard.buyButton)
        self.wait_and_assert_element_text(BuyWithACard.buyButton, buy_text)

    def select_graph_period(self, period):
        self.wait_and_click(GRAPH_PERIOD[period])
        self.wait_until_element_visible(Graph.table)
        self.wait_until_element_visible(Graph.chart)

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

    def check_value_in_deposit_address(self, value):
        self.assert_element_text_contains_value(DepositAddress.currentAddress, value)

    def check_value_not_in_deposit_address(self, value):
        self.assert_element_text_not_contains_value(DepositAddress.currentAddress, value)

    def check_new_deposit_address(self, current_address):
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
        time.sleep(1)
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
        #self.wait_until_element_visible(FILTER_BUTTON[history_filter])

    def remove_filter(self, history_filter):
        """
        Отключает фильтры на странице History
        :param history_filter: название фильтра, Exchange, Pay Out, Pay In, Failed
        """
        self.wait_and_click_element_within_element(FILTER_BUTTON[history_filter], Filters.removeFilter)
        self.wait_until_element_invisible(FILTER_BUTTON[history_filter], 0.5)