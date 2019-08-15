from Pages.BasePage import Page
from Locators.DashboardLocators import *
from Locators.TransactionsLocators import *
from Locators.SettingsLocators import *
import time
from Config.Users import *

WALLETFROM = {
    "BTC": Send.btcWallet,
    "ETH": Send.ethWallet,
}

class TransactionsPage(Page):
    def send_transaction_to_user_id(self, currency, amount, userID, comment):
        self.wait_and_click(WALLETFROM[currency])
        self.wait_and_click(Send.userIdOrEmail)
        self.wait_and_click(Send.continueButton1)
        self.wait_and_input_text(Send.sendToIdOrEmail, userID)
        self.wait_to_be_clickable(Send.continueButton2)
        self.wait_and_click(Send.continueButton2)
        self.wait_and_input_text(Send.amount, amount)
        self.wait_to_be_clickable(Send.continueButton3)
        self.wait_and_click(Send.continueButton3)
        self.wait_and_input_text(Send.comment, comment)
        self.wait_and_click(Send.withdraw)

    def check_first_transaction(self, currency, amount, comment):
        transactionTitle = "-%s %s" % (amount, currency)
        commentFormatted = 'Comment "%s"' % comment
        self.wait_and_assert_element_text(Send.firstTransactionAmount, transactionTitle)
        self.wait_and_assert_element_text(Send.firstTransactionComment, commentFormatted)

    def navigate_to_send(self):
        #TODO: дописать во все подобные методы проверку, что топ левел навигейшен кнопки выбраны или нет
        self.wait_and_click(WalletActionsButtons.send)

