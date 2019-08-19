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
        """
        Отправляет трансфер другому пользователю
        :param currency: кошелек с которого отправляется трансфер, BTC/ETH
        :param amount: string с количеством отправляемой валюты
        :param userID: User ID получателя трансфера, можно использовать email
        :param comment: комментарий к транзакции
        :return:
        """
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
        """
        Проверяет данные самой верхней транзакции в history
        :param currency: валюта транзакции, BTC/ETH
        :param amount: string с количеством валюты
        :param comment: комментарий к транзакции
        """
        transaction_title = "–%s %s" % (amount, currency)
        comment_formatted = 'Comment "%s"' % comment
        self.navigate_to_send()
        self.navigate_to_send()
        self.wait_and_assert_element_text(Send.firstTransactionAmount, transaction_title)
        self.wait_and_assert_element_text(Send.firstTransactionComment, comment_formatted)

    def navigate_to_send(self):
        """
        Переходит на страницу send с dashboard
        """
        #TODO: дописать во все подобные методы проверку, что топ левел навигейшен кнопки выбраны или нет
        self.wait_and_click(WalletActionsButtons.send)

    def navigate_to_history(self):
        """
        Переходит на страницу send с dashboard
        """
        #TODO: дописать во все подобные методы проверку, что топ левел навигейшен кнопки выбраны или нет
        self.wait_and_click(WalletActionsButtons.history)

    def check_not_verified_email_modal(self):
        self.wait_and_assert_element_text(Send.notVerifiedEmailModalMessage, "Email address is not verified")

