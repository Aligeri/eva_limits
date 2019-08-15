from Pages.BasePage import Page
from Locators.DashboardLocators import *
from Locators.SettingsLocators import *
import time
from Config.Users import *


class SettingsPage(Page):
    def check_email_is_not_verified(self, email):
        self.wait_and_click(NavigationButtons.settings)
        time.sleep(2)
        self.wait_and_click(NavigationLinks.account)
        currentEmail = self.get_element_attribute(Account.emailNotifications, "value")
        assert email == currentEmail
        self.wait_and_assert_element_text(Account.dangerText, "Verify email")

    def check_email_is_verified(self, email):
        self.wait_and_click(NavigationButtons.settings)
        self.wait_and_click(NavigationLinks.account)
        currentEmail = self.get_element_attribute(Account.emailNotifications, "value")
        assert email == currentEmail
        self.wait_and_assert_element_text(Account.successText, "Email is verified.")

