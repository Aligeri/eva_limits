from Pages.BasePage import Page
from Locators.DashboardLocators import *
from Locators.TransactionsLocators import *
from Locators.SecurityLocators import *
import re
import time
from selenium.common.exceptions import NoSuchElementException
import websocket

WALLETFROM = {
    "BTC": Send.btcWallet,
    "ETH": Send.ethWallet,
    "XRP": Send.xrpWallet,
    "DOGE": Send.dogeWallet,
    "XEM": Send.xemWallet,
}

COMPLEX_WALLET = {
    "XRP": Send.xrpWallet,
    "XEM": Send.xemWallet
}

DESTINATION_WALLET = {
    "XRP": Send.xrpRecieverWallet,
    "ETH": Send.ethRecieverWallet,
    "BTC": Send.btcRecieverWallet,
    "DOGE": Send.dogeWallet,
    "XEM": Send.xemRecieverWallet,
}


class TransactionsPage(Page):
    def send_transaction_step_1_user_id(self, currency):
        self.wait_and_click(WALLETFROM[currency])
        self.wait_and_click(Send.userIdOrEmail)
        self.wait_and_click(Send.continueButton1)

    def send_transaction_step_2_user_id(self, userID):
        self.wait_and_input_text(Send.sendToIdOrEmail, userID)
        self.wait_to_be_clickable(Send.continueButton2)
        self.wait_and_click(Send.continueButton2)

    def send_transaction_step_3(self, amount):
        self.wait_and_input_text(Send.amount, amount)
        self.wait_to_be_clickable(Send.continueButton3)
        self.wait_and_click(Send.continueButton3)

    def send_minimum_amount_step_3(self):
        self.wait_and_input_text(Send.amount, "0")
        amount_text = self.get_element_text(Send.limitExceededTooltip)
        amount = re.search("\d\.\d*", amount_text).group(0)
        self.clear_input_text(Send.amount)
        self.wait_and_input_text(Send.amount, amount)
        self.wait_to_be_clickable(Send.continueButton3)
        self.wait_and_click(Send.continueButton3)
        return amount

    def check_minimum_amount(self, amount):
        self.wait_and_input_text(Send.amount, amount)
        self.wait_and_assert_element_text(Send.limitExceededTooltip, "Minimum amount 0.00000001 BTC")

    def check_minimum_simple_amount(self, amount):
        self.wait_and_input_text(Send.amount, amount)
        self.wait_and_assert_element_text(Send.limitExceededTooltip, "Minimum amount 0.00000001 BTC")

    def send_transaction_step_4(self, comment):
        self.wait_and_input_text(Send.comment, comment)
        self.wait_and_click(Send.withdraw)

    def send_transaction_step_1_wallet_address(self, currency):
        self.wait_and_click(WALLETFROM[currency])
        self.wait_and_click(Send.userWalletAddress)
        self.wait_and_click(Send.continueButton1)

    def send_transaction_step_2_wallet_address(self, wallet_address, wallet_receiver):
        self.wait_and_input_text(Send.sendToAddress, wallet_address)
        self.wait_and_click(DESTINATION_WALLET[wallet_receiver])
        self.wait_to_be_clickable(Send.continueButton2)
        self.wait_and_click(Send.continueButton2)

    def send_complex_transaction_step_1(self, currency):
        self.wait_and_click(COMPLEX_WALLET[currency])
        self.wait_and_click(Send.userWalletAddress)
        self.wait_and_click(Send.continueButton1)

    def send_complex_transaction_step_2(self, currency, wallet_address, wallet_tag):
        self.wait_and_input_text(Send.sendToAddress, wallet_address)
        self.wait_and_click(DESTINATION_WALLET[currency])
        self.wait_and_input_text(Send.destinationTag, wallet_tag)
        self.wait_to_be_clickable(Send.continueButton2)
        self.wait_and_click(Send.continueButton2)

    def send_fiat_transaction_step_3(self, amount):
        self.wait_and_click(Send.changeToFiat)
        self.wait_and_input_text(Send.amount, amount)
        self.wait_to_be_clickable(Send.continueButton3)
        self.wait_and_click(Send.continueButton3)

    def check_fiat_transaction_step_4(self, amount):
        amountfix = "≈ $" + amount
        value = self.get_element_text(Send.fiatAmount)
        assert amountfix == value

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

    def send_transaction_to_blocked_address(self, currency, wallet_address):
        """
        Отправляет трансфер на адрес запрещенного токена ETH
        :param currency: кошелек с которого отправляется трансфер ETH
        :param amount: string с количеством отправляемой валюты
        :param wallet_address: Wallet address получателя трансфера
        :param comment: комментарий к транзакции
        :return:
        """
        self.wait_and_click(WALLETFROM[currency])
        self.wait_and_click(Send.userWalletAddress)
        self.wait_and_click(Send.continueButton1)
        self.wait_and_input_text(Send.sendToAddress, wallet_address)
        self.wait_and_assert_element_text(Send.tokenError, "Sorry we don’t support this token.")


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
        retries = 2
        while retries > 0:
            try:
                text = self.get_element_text(Send.networkFee)
                number = re.search("\d\.\d*", text).group(0)
                return number
            except:
                time.sleep(0.5)
                retries -= 1
        raise ValueError("Network fee is not found")


    def __get_arrival_amount(self):
        retries = 2
        while retries > 0:
            try:
                text = self.get_element_text(Send.arrivalAmount)
                number = re.search("\d\.\d*", text).group(0)
                return number
            except:
                time.sleep(0.5)
                retries -= 1
        raise ValueError("Arrival amount is not found")


    def __get_total_amount(self):
        retries = 2
        while retries > 0:
            try:
                text = self.get_element_text(Send.totalWithFee)
                number = re.search("\d\.\d*", text).group(0)
                return number
            except:
                time.sleep(0.5)
                retries -= 1
        raise ValueError("Total amount is not found")


    def check_BTC_Fee(self, fee_type, amount):
        FEE_TYPE = {
            "Low" : Send.lowFee,
            "Normal": Send.normalFee,
            "Fast": Send.fastFee,
            "Urgent": Send.urgentFee
        }
        self.wait_and_click(FEE_TYPE[fee_type])
        time.sleep(0.5)
        network_fee = self.__get_network_fee()
        arrival_amount = self.__get_arrival_amount()
        total_amount = self.__get_total_amount()
        a = float(network_fee) + float(arrival_amount)
        b = float(total_amount)
        assert a == b

        #self.wait_and_assert_element_text(Send.totalWithFee, amount_text)

    def check_exclude_fee(self):
        """
        Проверяет правильность расчета fee при exclude
        :return:
        """
        network_fee = self.__get_network_fee()
        arrival_amount = self.__get_arrival_amount()
        total_amount = self.__get_total_amount()
        a = float(network_fee) + float(arrival_amount)
        b = float(total_amount)
        assert a == b

    def check_include_fee(self):
        """
        Проверяет правильность расчета fee при include
        :return:
        """
        network_fee = self.__get_network_fee()
        arrival_amount = self.__get_arrival_amount()
        total_amount = self.__get_total_amount()
        a = float(total_amount) - float(network_fee)
        b = float(arrival_amount)
        assert a == b

    def send_complex_transaction_to_user_id(self, currency, amount, wallet_address, wallet_tag, comment):
        """
        Отправляет трансфер в составной валюте на wallet address
        :param currency: кошелек с которого отправляется трансфер в составной валюте, XRP
        :param amount: string с количеством отправляемой валюты
        :param wallet_address: Wallet address получателя трансфера
        :param wallet_tag: Destination tag получателя трансфера
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
        :param currency: валюта транзакции, BTC/ETH/DOGE
        :param amount: string с количеством валюты
        :param comment: комментарий к транзакции
        """
        transaction_title = "–%s %s" % (amount, currency)
        comment_formatted = 'Comment "%s"' % comment
        retries_left = 5
        while retries_left > 0:
            try:
                self.wait_until_element_visible(Send.firstTransaction)
                self.assert_element_text(Send.firstTransactionComment, comment_formatted)
                self.assert_element_text(Send.firstTransactionAmount, transaction_title)
                return
            except:
                self.navigate_to_send()
                self.navigate_to_history()
                retries_left -= 1
        raise NoSuchElementException("transaction is not found")

    def assert_transactions_page_displayed(self):
        self.wait_until_element_visible(Send.firstTransaction)

    def find_transaction_by_comment(self, currency, amount, comment):
        """
        Проверяет данные самой верхней транзакции в history
        :param currency: валюта транзакции, BTC/ETH/DOGE
        :param amount: string с количеством валюты
        :param comment: комментарий к транзакции
        """
        transaction_title = "–%s %s" % (amount, currency)
        comment_formatted = 'Comment "%s"' % comment
        retries_left = 10
        while retries_left > 0:
            try:
                self.wait_until_element_visible((By.XPATH, (
                        ".//a[contains(@class, 'item__wrapper--2HY-h')][.//div[contains(text(), '%s')]]" % comment_formatted)),
                                                10)
                self.wait_until_element_visible((By.XPATH, (
                        ".//a[contains(@class, 'item__wrapper--2HY-h')][.//div[contains(text(), '%s')]]" % transaction_title)),
                                                10)
                return
            except:
                self.navigate_to_send()
                self.navigate_to_history()
                retries_left -= 1
        raise NoSuchElementException("transaction is not found")

    def find_simple_by_comment(self, currency, amount, comment):
        """
        Проверяет данные самой верхней транзакции в history
        :param currency: валюта транзакции, BTC/ETH/DOGE
        :param amount: string с количеством валюты
        :param comment: комментарий к транзакции
        """
        transaction_title = "–%s %s" % (amount, currency)
        comment_formatted = 'Comment "%s"' % comment
        retries_left = 10
        while retries_left > 0:
            try:
                self.wait_until_element_visible((By.XPATH, (
                        ".//a[contains(@class, 'item__wrapper--2HY-h')][.//div[contains(text(), '%s')]]" % comment_formatted)),
                                                10)
                self.wait_until_element_visible((By.XPATH, (
                        ".//a[contains(@class, 'item__wrapper--2HY-h')][.//div[contains(text(), '%s')]]" % transaction_title)),
                                                10)
                return
            except:
                self.navigate_to_send()
                self.navigate_to_history()
                retries_left -= 1
        raise NoSuchElementException("transaction is not found")


    def check_first_transaction_receive(self, currency, amount, comment):
        """
        Проверяет данные самой верхней транзакции в history
        :param currency: валюта транзакции, BTC/ETH
        :param amount: string с количеством валюты
        :param comment: комментарий к транзакции
        """
        transaction_title = "+%s %s" % (amount, currency)
        comment_formatted = 'Comment "%s"' % comment
        retries_left = 5
        while retries_left > 0:
            try:
                self.wait_until_element_visible((By.XPATH, (
                        ".//a[contains(@class, 'item__wrapper--2HY-h')][.//div[contains(text(), '%s')]]" % comment_formatted)),
                                                10)
                self.wait_until_element_visible((By.XPATH, (
                        ".//a[contains(@class, 'item__wrapper--2HY-h')][.//div[contains(text(), '%s')]]" % transaction_title)),
                                                10)
                return
            except:
                self.navigate_to_send()
                self.navigate_to_history()
                retries_left -= 1
        raise NoSuchElementException("transaction is not found")

    def check_first_transaction_comment(self, comment):
        """
        Проверяет комментарий самой верхней транзакции в history
        :param comment: комментарий к транзакции
        """
        retries_left = 5
        while retries_left > 0:
            try:
                self.wait_until_element_visible(Send.firstTransaction)
                self.assert_element_text(Send.firstTransactionComment, comment)
                return
            except:
                self.navigate_to_send()
                self.navigate_to_history()
                retries_left -= 1
        raise NoSuchElementException("transaction is not found")

    def check_failed_transaction(self):
        """
        Проверяет данные внутри упавшей транзакции в history
        """

        self.wait_and_click(Send.firstErrorTransaction)
        self.wait_and_assert_element_text(Send.errorMessageInTransaction, "You cannot send circularly eth to your pay in address")

    def check_doublespending_transaction(self, comment):
        """
        Проверяет данные внутри упавшей транзакции даблспендинга в history
        """
        comment_formatted = 'Comment "%s"' % comment
        self.wait_and_click((By.XPATH, (
                ".//a[contains(@class, 'item__wrapper--2HY-h')][.//div[contains(text(), '%s')]]" % comment_formatted)))
        self.wait_and_assert_element_text(Send.errorMessageInTransaction, "Too many similar requests. Try again")


    def check_frozen_transaction(self):
        """
        Проверяет данные внутри упавшей транзакции в history
        """

        self.wait_and_click(Send.firstErrorTransaction)
        self.wait_and_assert_element_text(Send.errorMessageInTransaction, "After changing your password, you must wait 24 hours to start making transactions again.")

    def check_unconfirmed_transaction(self, comment):
        """
        Проверяет данные внутри упавшей транзакции в history
        """
        self.open_transaction_by_comment(comment)
        self.wait_and_assert_element_text(Send.statusInTransaction, "Requires email confirmation")
        time.sleep(1)

    def cancel_transaction(self):
        self.wait_and_click(Send.cancelButtonInTransaction)

    def check_canceled_transaction(self, comment, reason):
        #self.navigate_to_send()
        #self.navigate_to_history()
        self.open_failed_transaction_by_comment(comment)
        self.wait_and_assert_element_text(Send.errorMessageInTransaction, reason)


    def open_transaction_by_comment(self, comment):
        retries_left = 5
        while retries_left > 0:
            try:
                self.wait_until_element_visible((By.XPATH, (
                            ".//a[contains(@class, 'item__wrapper--2HY-h')][.//div[contains(text(), '%s')]]" % comment)),
                                                10)
                self.wait_and_click((By.XPATH, (
                            ".//a[contains(@class, 'item__wrapper--2HY-h')][.//div[contains(text(), '%s')]]" % comment)))
                return
            except:
                self.navigate_to_send()
                self.navigate_to_history()
                retries_left -= 1
        raise NoSuchElementException("transaction is not found")


    def open_failed_transaction_by_comment(self, comment):
        retries_left = 5
        while retries_left > 0:
            try:
                self.wait_until_element_visible((By.XPATH, (".//a[contains(@class, 'item__wrapper__failed--16kTs')][.//div[contains(text(), '%s')]]" % comment)), 10)
                self.wait_and_click((By.XPATH, (".//a[contains(@class, 'item__wrapper__failed--16kTs')][.//div[contains(text(), '%s')]]" % comment)))
                return
            except:
                self.navigate_to_send()
                self.navigate_to_history()
                retries_left -= 1
        raise NoSuchElementException("transaction is not found")

    def cancel_first_transaction_without_hash(self, comment):
        self.open_transaction_by_comment(comment)
        self.wait_and_click(Send.cancelButtonInTransaction)
        self.open_failed_transaction_by_comment(comment)
        self.wait_and_assert_element_text(Send.errorMessageInTransaction, "Canceled transaction")

    def cancel_first_transaction(self):
        self.wait_and_click(Send.cancelButtonInTransaction)
        self.wait_and_click(Send.firstErrorTransaction)
        self.wait_and_assert_element_text(Send.errorMessageInTransaction, "Email confirmation canceled by user")

    def send_top_up_phone_transaction(self, phone):
        self.wait_and_input_text(TopUpPhone.mobileNumber, phone)
        self.wait_to_be_clickable(TopUpPhone.continueButton, 20)
        self.wait_and_click(TopUpPhone.continueButton)
        self.wait_and_click(TopUpPhone.firstPaymentValue)
        self.wait_and_click(TopUpPhone.sendCoinsButton)
        self.wait_until_element_visible(TopUpPhone.successModal)

    def check_top_up_phone_validation(self, phone, validation, validation_message=''):
        self.wait_and_input_text(TopUpPhone.mobileNumber, phone)
        if validation:
            button_state = self.get_element_attribute(TopUpPhone.continueButton, "disabled")
            print(button_state)
            assert button_state == "true"
        else:
            self.wait_to_be_clickable(TopUpPhone.continueButton, 20)
        if validation_message is not '':
            self.wait_until_element_visible(TopUpPhone.errorMessage)
            text = self.get_element_text(TopUpPhone.errorMessage)
            assert text == validation_message

    def check_bitrefill_operator(self, operator):
        self.wait_until_element_visible(TopUpPhone.logo)
        alt = self.get_element_attribute(TopUpPhone.logo, "alt")
        url = self.get_element_attribute(TopUpPhone.logo, "src")
        if operator == "MTS":
            assert alt == "MTS Russia"
            assert url == "https://www.bitrefill.com/content/cn/d_operator.png/mts-russia"
        if operator == "Tele2":
            assert alt == "Tele2 Russia"
            assert url == "https://www.bitrefill.com/content/cn/d_operator.png/tele2-russia"





    def navigate_to_send(self):
        """
        Переходит на страницу send с dashboard
        """
        #TODO: дописать во все подобные методы проверку, что топ левел навигейшен кнопки выбраны или нет
        self.wait_and_click(WalletActionsButtons.send)


    def navigate_to_top_up_phone(self):
        self.wait_and_click(WalletActionsButtons.topUpPhone)

    def navigate_to_history(self):
        """
        Переходит на страницу send с dashboard
        """
        #TODO: дописать во все подобные методы проверку, что топ левел навигейшен кнопки выбраны или нет
        self.wait_and_click(WalletActionsButtons.history)

    def check_not_verified_email_modal(self):
        self.wait_and_assert_element_text(Send.notVerifiedEmailModalMessage, "Email address is not verified")

    def check_limit_exceeded_transaction(self, currency, amount, userID):
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
        self.wait_and_assert_element_text(Send.limitExceededTooltip, "Limit exceeded")
        self.assert_element_attirbute_value(Send.continueButton3, "disabled", "true")

    def get_new_email_transfer_password(self, create_password_link):
        self.driver.get(create_password_link)
        password = self.get_element_text(Send.newEmailTransferPassword)
        return password

    def input_2fa_and_send_transaction(self, code):
        code_by_char = list(code)
        self.wait_and_input_text(TwoFactorAuth.code1, code_by_char[0])
        self.wait_and_input_text(TwoFactorAuth.code2, code_by_char[1])
        self.wait_and_input_text(TwoFactorAuth.code3, code_by_char[2])
        self.wait_and_input_text(TwoFactorAuth.code4, code_by_char[3])
        self.wait_and_input_text(TwoFactorAuth.code5, code_by_char[4])
        self.wait_and_input_text(TwoFactorAuth.code6, code_by_char[5])
        self.wait_and_click(Send.confirm2fa)

    def check_transactions_on_page(self, comment, amount):
        transactions = self.get_elements(Send.transactionBlock)
        comments = []
        amounts = []
        for transaction in transactions:
            comments.append(self.get_element_text_within_webelement(transaction, Send.commentBlock))
            amounts.append(self.get_element_text_within_webelement(transaction, Send.amountBlock))
        assert comment == comments
        assert amount == amounts

    def check_unconfirmed_transaction_by_comment(self, comment):
        """
        проверяет, что транзакция подвисла в фиолетовом статусе ожидания мультисиг
        не переходя в детали транзакции
        """
        retries_left = 5
        while retries_left > 0:
            try:
                self.wait_until_element_visible((By.XPATH, (
                            ".//a[contains(@class, 'item__wrapper--2HY-h item__wrapper__unconfirmed--3YAln')][.//div[contains(text(), '%s')]]" % comment)),
                                                10)
                return
            except:
                self.navigate_to_send()
                self.navigate_to_history()
                retries_left -= 1
        raise NoSuchElementException("transaction is not found")

    def check_completed_transaction(self, comment):
        """
        Проверяет что транзакция закомплитилась
        """
        self.open_transaction_by_comment(comment)
        self.wait_and_assert_element_text(Send.statusInTransaction, "Completed")
        time.sleep(1)