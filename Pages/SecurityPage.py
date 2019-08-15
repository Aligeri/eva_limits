from Pages.BasePage import Page
from Locators.DashboardLocators import *
from Locators.SecurityLocators import *
import time
from Config.Users import *


class SecurityPage(Page):
    def navigate_to_pincode(self):
        self.wait_and_click(NavigationButtons.security)
        self.wait_and_click(NavigationLinks.pincode)

    def input_security_pincode_current(self, pincode):
        pin_by_char = list(pincode)
        self.wait_and_input_text(SecurityPincode.current1, pin_by_char[0])
        self.wait_and_input_text(SecurityPincode.current2, pin_by_char[1])
        self.wait_and_input_text(SecurityPincode.current3, pin_by_char[2])
        self.wait_and_input_text(SecurityPincode.current4, pin_by_char[3])

    def input_security_pincode_new(self, pincode):
        pin_by_char = list(pincode)
        self.wait_and_input_text(SecurityPincode.new1, pin_by_char[0])
        self.wait_and_input_text(SecurityPincode.new2, pin_by_char[1])
        self.wait_and_input_text(SecurityPincode.new3, pin_by_char[2])
        self.wait_and_input_text(SecurityPincode.new4, pin_by_char[3])

    def input_security_pincode_repeat(self, pincode):
        pin_by_char = list(pincode)
        self.wait_and_input_text(SecurityPincode.repeat1, pin_by_char[0])
        self.wait_and_input_text(SecurityPincode.repeat2, pin_by_char[1])
        self.wait_and_input_text(SecurityPincode.repeat3, pin_by_char[2])
        self.wait_and_input_text(SecurityPincode.repeat4, pin_by_char[3])

    def navigate_to_limits(self):
        self.wait_and_click(NavigationButtons.security)
        self.wait_and_click(NavigationLinks.limits)

    def create_new_weekly_limit(self, currency, amount):
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
        activeLimit = "%s %s / 24h" % (amount, currency)
        self.wait_and_assert_element_text(LimitModal.activeLimit, activeLimit)
        availableAmount = "%s %s" % (amount, currency)
        self.wait_and_assert_element_text(LimitModal.availableAmount, availableAmount)


    def change_limit_after_creation(self, amount):
        self.wait_and_click(LimitModal.changeLimit)
        self.wait_and_input_text(LimitModal.amount, amount)
        self.wait_and_click(LimitModal.changeLimitConfirm)
        self.wait_and_click(LimitModal.set)
        self.wait_and_assert_element_text(LimitModal.pendingChange, "Limit settings will be changed in in 2 days")

    def disable_limit_after_creation(self):
        self.wait_and_click(LimitModal.disableLimit)
        self.wait_and_click(LimitModal.disableLimitConfirm)
        self.wait_and_assert_element_text(LimitModal.pendingChange, "Limit settings will be changed in in 2 days")
