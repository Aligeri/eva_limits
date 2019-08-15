from Pages.BasePage import Page
from Locators.DashboardLocators import *
from Locators.WalletLocators import *


class DashboardPage(Page):
    def select_language(self, language):
        pass

    def navigate_to_receive(self):
        self.wait_and_click(WalletActionsButtons.receive)

    def select_wallet(self, wallet):
        WALLET = {
            "Ardor": ReceiveWallets.ardr,
            "Bitcoin": ReceiveWallets.btc,
            "Bitcoin Cash": ReceiveWallets.bcc,
        }
        self.wait_and_click(WALLET[wallet])

    def assert_deposit_address_is_not_empty(self):
        self.assert_element_text_is_not_empty(DepositAddress.currentAddress)

    def get_current_deposit_address(self):
        return self.get_element_attribute(DepositAddress.currentAddress, "text()")

    def generate_new_deposit_address(self, current_address):
        self.wait_and_click(DepositAddress.generateNew)
        self.assert_element_text_is_not_equal(DepositAddress.currentAddress, current_address)

    def check_previous_address_in_list(self, current_address):
        self.wait_and_click(DepositAddress.showAll)
        previous_address = self.get_element_attribute(DepositAddress.previousAddress2, "text()")
        assert previous_address == current_address
