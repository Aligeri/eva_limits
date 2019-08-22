from Pages.BasePage import Page
from Locators.DashboardLocators import *
from Locators.TransactionsLocators import *
import re
import time

WALLETFROM = {
    "BTC": Send.btcWallet,
    "ETH": Send.ethWallet,
}

COMPLEX_WALLET = {
    "XRP": Send.xrpWallet
}

DESTINATION_WALLET = {
    "XRP": Send.xrpRecieverWallet,
    "ETH": Send.ethRecieverWallet,
    "BTC": Send.btcRecieverWallet,
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

    def send_transaction_to_wallet_address(self, currency, amount, wallet_address, waller_receiver, comment):
        """
        Отправляет трансфер другому пользователю
        :param currency: кошелек с которого отправляется трансфер, BTC/ETH
        :param amount: string с количеством отправляемой валюты
        :param wallet_address: Wallet address получателя трансфера
        :param comment: комментарий к транзакции
        :return:
        """
        self.wait_and_click(WALLETFROM[currency])
        self.wait_and_click(Send.userWalletAddress)
        self.wait_and_click(Send.continueButton1)
        self.wait_and_input_text(Send.sendToAddress, wallet_address)
        self.wait_and_click(DESTINATION_WALLET[waller_receiver])
        self.wait_to_be_clickable(Send.continueButton2)
        self.wait_and_click(Send.continueButton2)
        self.wait_and_input_text(Send.amount, amount)
        self.wait_to_be_clickable(Send.continueButton3)
        self.wait_and_click(Send.continueButton3)
        self.wait_and_input_text(Send.comment, comment)
        self.wait_and_click(Send.withdraw)

    def show_fee_for_wallet_address(self, currency, amount, wallet_address, waller_receiver):
        """
        Отправляет трансфер другому пользователю
        :param currency: кошелек с которого отправляется трансфер, BTC/ETH
        :param amount: string с количеством отправляемой валюты
        :param wallet_address: Wallet address получателя трансфера
        :param comment: комментарий к транзакции
        :return:
        """
        self.wait_and_click(WALLETFROM[currency])
        self.wait_and_click(Send.userWalletAddress)
        self.wait_and_click(Send.continueButton1)
        self.wait_and_input_text(Send.sendToAddress, wallet_address)
        self.wait_and_click(DESTINATION_WALLET[waller_receiver])
        self.wait_to_be_clickable(Send.continueButton2)
        self.wait_and_click(Send.continueButton2)
        self.wait_and_input_text(Send.amount, amount)

    def __get_network_fee(self):
        text = self.get_element_text(Send.networkFee)
        number = re.search("\d\.\d*", text).group(0)
        return number

    def __get_arrival_amount(self):
        text = self.get_element_text(Send.arrivalAmount)
        number = re.search("\d\.\d*", text).group(0)
        return number

    def __get_total_amount(self):
        text = self.get_element_text(Send.totalWithFee)
        number = re.search("\d\.\d*", text).group(0)
        return number

    def check_BTC_Fee(self, fee_type, amount):
        FEE_TYPE = {
            "Low" : Send.lowFee,
            "Normal": Send.normalFee,
            "Fast": Send.fastFee,
            "Urgent": Send.urgentFee
        }
        self.wait_and_click(FEE_TYPE[fee_type])
        amount_text = "%s BTC" % amount
        self.wait_and_assert_element_text(Send.totalWithFee, amount_text)

    def check_exclude_fee(self):
        network_fee = self.__get_network_fee()
        arrival_amount = self.__get_arrival_amount()
        total_amount = self.__get_total_amount()
        a = float(network_fee) + float(arrival_amount)
        b = float(total_amount)
        assert a == b

    def check_include_fee(self):
        network_fee = self.__get_network_fee()
        arrival_amount = self.__get_arrival_amount()
        total_amount = self.__get_total_amount()
        a = float(total_amount) - float(network_fee)
        b = float(arrival_amount)
        assert a == b



    def send_complex_transaction_to_user_id(self, currency, amount, wallet_address, wallet_tag, comment):
        """
        Отправляет трансфер другому пользователю
        :param currency: кошелек с которого отправляется трансфер в составной валюте, XRP
        :param amount: string с количеством отправляемой валюты
        :param userID: User ID получателя трансфера, можно использовать email
        :param comment: комментарий к транзакции
        :return:
        """
        self.wait_and_click(COMPLEX_WALLET[currency])
        self.wait_and_click(Send.userWalletAddress)
        self.wait_and_click(Send.continueButton1)
        self.wait_and_input_text(Send.sendToAddress, wallet_address)
        self.wait_and_click(DESTINATION_WALLET[currency])
        self.wait_and_input_text(Send.destinationTag, wallet_tag)
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
        self.navigate_to_history()
        self.wait_and_assert_element_text(Send.firstTransactionAmount, transaction_title)
        self.wait_and_assert_element_text(Send.firstTransactionComment, comment_formatted)

    def check_failed_transaction(self):
        """
        Проверяет данные самой верхней транзакции в history
        :param currency: валюта транзакции, BTC/ETH
        :param amount: string с количеством валюты
        :param comment: комментарий к транзакции
        """
        #transaction_title = "–%s %s" % (amount, currency)
        #comment_formatted = 'Comment "%s"' % comment
        self.navigate_to_send()
        self.navigate_to_history()
        self.wait_and_click(Send.firstErrorTransaction)
        self.wait_and_assert_element_text(Send.errorMessageInTransaction, "Cannot send eth to yourself pay in address")

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

