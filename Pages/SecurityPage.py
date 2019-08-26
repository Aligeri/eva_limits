from Pages.BasePage import Page
from Locators.DashboardLocators import *
from Locators.SecurityLocators import *
import time


class SecurityPage(Page):
    def navigate_to_pincode(self):
        self.wait_and_click(NavigationButtons.security)
        self.wait_and_click(NavigationLinks.pincode)

    def input_security_pincode_current(self, pincode):
        """
        Ввод текущего пин-кода при изменении пин-кода
        :param pincode: пин-код вида string из 4 цифр
        """
        pin_by_char = list(pincode)
        self.wait_and_input_text(SecurityPincode.current1, pin_by_char[0])
        self.wait_and_input_text(SecurityPincode.current2, pin_by_char[1])
        self.wait_and_input_text(SecurityPincode.current3, pin_by_char[2])
        self.wait_and_input_text(SecurityPincode.current4, pin_by_char[3])

    def input_security_pincode_new(self, pincode):
        """
        Ввод нового пин-кода при изменении пин-кода
        :param pincode: пин-код вида string из 4 цифр
        """
        pin_by_char = list(pincode)
        self.wait_and_input_text(SecurityPincode.new1, pin_by_char[0])
        self.wait_and_input_text(SecurityPincode.new2, pin_by_char[1])
        self.wait_and_input_text(SecurityPincode.new3, pin_by_char[2])
        self.wait_and_input_text(SecurityPincode.new4, pin_by_char[3])

    def input_security_pincode_repeat(self, pincode):
        """
        Повтор нового пин-кода при изменении пин-кода
        :param pincode: пин-код вида string из 4 цифр
        """
        pin_by_char = list(pincode)
        self.wait_and_input_text(SecurityPincode.repeat1, pin_by_char[0])
        self.wait_and_input_text(SecurityPincode.repeat2, pin_by_char[1])
        self.wait_and_input_text(SecurityPincode.repeat3, pin_by_char[2])
        self.wait_and_input_text(SecurityPincode.repeat4, pin_by_char[3])

    def navigate_to_limits(self):
        """
        Переходит на страницу security > limits с дашборда
        :return:
        """
        self.wait_and_click(NavigationButtons.security)
        self.wait_and_click(NavigationLinks.limits)

    def create_new_weekly_limit(self, currency, amount):
        """
        Создает новый лимит на странице Security/Limits
        :param currency: валюта на которую создается лимит, BTC/FWH/ARDR
        :param amount: string с размером лимита
        """
        WALLET = {
            "FWH": LimitWallets.fwt,
            "BTC": LimitWallets.btc,
            "ARDR": LimitWallets.ardr,
        }
        self.wait_and_click(WALLET[currency])
        self.wait_and_input_text(LimitModal.amount, amount)
        self.wait_and_click(LimitModal.perWeek)
        self.wait_and_click(LimitModal.setLimit)
        self.wait_and_click(LimitModal.set)
        active_limit = "%s %s / 24h" % (amount, currency)
        self.wait_and_assert_element_text(LimitModal.activeLimit, active_limit)
        available_amount = "%s %s" % (amount, currency)
        self.wait_and_assert_element_text(LimitModal.availableAmount, available_amount)

    def change_limit_after_creation(self, amount):
        """
        Меняет лимит сразу после создания (модалка лимита должна быть открыта)
        Проверяет что показано оповещение что лимит будет изменен через 2 дня
        :param amount: новый размер лимита
        """
        self.wait_and_click(LimitModal.changeLimit)
        self.wait_and_input_text(LimitModal.amount, amount)
        self.wait_to_be_clickable(LimitModal.changeLimitConfirm)
        self.wait_and_click(LimitModal.changeLimitConfirm)
        self.wait_and_click(LimitModal.set)
        self.wait_and_assert_element_text(LimitModal.pendingChange, "Limit settings will be changed in in 2 days")

    def disable_limit_after_creation(self):
        """
        Отключает лимит сразу после создания (модалка лимита должна быть открыта)
        Проверяет что показано оповещение что лимит будет изменен через 2 дня
        """
        self.wait_and_click(LimitModal.disableLimit)
        self.wait_and_click(LimitModal.disableLimitConfirm)
        self.wait_and_assert_element_text(LimitModal.pendingChange, "Limit settings will be changed in in 2 days")

    def close_limit_modal(self):
        self.wait_and_click(LimitModal.overlay)

    def check_BTC_limit_percent(self, percent):
        self.wait_and_assert_element_text(LimitModal.BTCLimitPercent, percent)

    def navigate_to_email_confirmation(self):
        self.wait_and_click(NavigationButtons.security)
        self.wait_and_click(NavigationLinks.emailConfirmation)

    def add_multisig_address(self, email):
        """
        Добавляет multisig емейл на странице Security > Email confirmation
        :param email: емейл который добавляется в качестве multisig
        :return:
        """
        self.assert_element_attirbute_value(Multisig.continueButton, "disabled", "true")
        time.sleep(1)
        self.wait_and_input_text(Multisig.email1, email)
        self.wait_and_click(Multisig.gotIt)
        self.wait_and_click(Multisig.continueButton)


    def discard_multisig_address(self):
        """
        Удаляет неподтвержденные multisig емейлы на странице Security > Email confirmation
        :return:
        """
        self.wait_until_element_visible(Multisig.disclaimer)
        self.wait_and_click(Multisig.disclaimerDiscard)
        self.assert_element_attirbute_value(Multisig.email1, "value", "")


