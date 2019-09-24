from Pages.BasePage import Page
from Locators.DashboardLocators import *
from Locators.SecurityLocators import *
import time


class SecurityPage(Page):
    def navigate_to_pincode(self):
        self.wait_and_click(NavigationButtons.security)
        self.wait_and_click(NavigationLinks.pincode)

    def navigate_to_2fa(self):
        self.wait_and_click(NavigationButtons.security)
        self.wait_and_click(NavigationLinks.twoFactorAuthentication)


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
        self.wait_until_element_invisible(LimitModal.setLimit, 1)
        self.wait_to_be_clickable(LimitModal.set)
        self.wait_and_click(LimitModal.set)
        active_limit = "%s %s / 24h" % (amount, currency)
        self.wait_and_assert_element_text(LimitModal.activeLimit, active_limit)
        available_amount = "%s %s" % (amount, currency)
        self.wait_and_assert_element_text(LimitModal.availableAmount, available_amount)

    def change_limit_after_creation(self, amount, currency):
        """
        Меняет лимит сразу после создания (модалка лимита должна быть открыта)
        Проверяет что показано оповещение что лимит будет изменен через 2 дня
        :param amount: новый размер лимита
        """
        WALLET = {
            "FWH": LimitWallets.fwt,
            "BTC": LimitWallets.btc,
            "ARDR": LimitWallets.ardr,
        }
        self.wait_and_click(WALLET[currency])
        self.wait_and_click(LimitModal.changeLimit)
        self.wait_and_input_text(LimitModal.amount, amount)
        self.wait_to_be_clickable(LimitModal.changeLimitConfirm)
        self.wait_and_click(LimitModal.changeLimitConfirm)
        self.wait_and_click(LimitModal.set)
        self.wait_and_assert_element_text(LimitModal.pendingChange, "Limit settings will be changed in in 2 days")

    def disable_limit_after_creation(self, currency):
        """
        Отключает лимит сразу после создания (модалка лимита должна быть открыта)
        Проверяет что показано оповещение что лимит будет изменен через 2 дня
        """
        WALLET = {
            "FWH": LimitWallets.fwt,
            "BTC": LimitWallets.btc,
            "ARDR": LimitWallets.ardr,
        }
        self.wait_and_click(WALLET[currency])
        self.wait_and_click(LimitModal.disableLimit)
        self.wait_and_click(LimitModal.disableLimitConfirm)
        self.wait_and_assert_element_text(LimitModal.pendingChange, "Limit settings will be changed in in 2 days")

    def check_limit_buttons_are_not_displayed(self, currency):
        """
        Меняет лимит сразу после создания (модалка лимита должна быть открыта)
        Проверяет что показано оповещение что лимит будет изменен через 2 дня
        :param amount: новый размер лимита
        """
        WALLET = {
            "FWH": LimitWallets.fwt,
            "BTC": LimitWallets.btc,
            "ARDR": LimitWallets.ardr,
        }
        self.wait_and_click(WALLET[currency])
        self.wait_and_assert_element_text(LimitModal.pendingChange, "Limit settings will be changed in in 2 days")

    def close_limit_modal(self):
        self.wait_until_element_visible(LimitModal.overlay)
        self.hover_and_click(LimitModal.overlay)

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
        self.wait_until_element_visible(Multisig.stats)
        time.sleep(0.5)
        self.assert_element_attirbute_value(Multisig.continueButton, "disabled", "true")
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

    def disable_multisig(self):
        self.wait_until_element_visible(Multisig.disclaimerDisable)
        self.wait_and_click(Multisig.disclaimerDisable)

    def get_2fa_activation_code(self):
        self.wait_and_click(TwoFactorAuth.continueButton)
        code = self.get_element_text(TwoFactorAuth.activationCode)
        return code

    def input_2fa(self, code):
        code_by_char = list(code)
        self.wait_and_input_text(TwoFactorAuth.code1, code_by_char[0])
        self.wait_and_input_text(TwoFactorAuth.code2, code_by_char[1])
        self.wait_and_input_text(TwoFactorAuth.code3, code_by_char[2])
        self.wait_and_input_text(TwoFactorAuth.code4, code_by_char[3])
        self.wait_and_input_text(TwoFactorAuth.code5, code_by_char[4])
        self.wait_and_input_text(TwoFactorAuth.code6, code_by_char[5])

    def check_2fa_checkbox_state(self, checkbox, state):
        """
        Проверяет состояние чекбокса 2фа
        :param checkbox: login/payout/export
        :param state: enabled/disabled
        :return:
        """
        CHECKBOX = {
            "login": TwoFactorAuth.loginCheckboxState,
            "payout": TwoFactorAuth.payoutCheckboxState,
            "export": TwoFactorAuth.exportCheckboxState
        }
        checkboxState = self.get_element_attribute(CHECKBOX[checkbox], "checked")
        if state == "enabled":
            assert checkboxState == "true"
        if state == "disabled":
            assert checkboxState is None

    def enable_2fa_checkbox(self, checkbox):
        CHECKBOX_STATE = {
            "login": TwoFactorAuth.loginCheckboxState,
            "payout": TwoFactorAuth.payoutCheckboxState,
            "export": TwoFactorAuth.exportCheckboxState
        }
        CHECKBOX = {
            "login": TwoFactorAuth.loginCheckbox,
            "payout": TwoFactorAuth.payoutCheckbox,
            "export": TwoFactorAuth.exportCheckbox
        }
        checkboxState = self.get_element_attribute(CHECKBOX_STATE[checkbox], "checked")
        if checkboxState == "true":
            return
        if checkboxState is None:
            self.wait_and_click(CHECKBOX[checkbox])

    def disable_2fa_checkbox(self, checkbox, code):
        CHECKBOX_STATE = {
            "login": TwoFactorAuth.loginCheckboxState,
            "payout": TwoFactorAuth.payoutCheckboxState,
            "export": TwoFactorAuth.exportCheckboxState
        }
        CHECKBOX = {
            "login": TwoFactorAuth.loginCheckbox,
            "payout": TwoFactorAuth.payoutCheckbox,
            "export": TwoFactorAuth.exportCheckbox
        }
        checkboxState = self.get_element_attribute(CHECKBOX_STATE[checkbox], "checked")
        if checkboxState == "true":
            self.wait_and_click(CHECKBOX[checkbox])
            self.input_2fa(code)
            self.wait_and_click(TwoFactorAuth.disableModal)
        if checkboxState is None:
            return