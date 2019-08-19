from Pages.BasePage import Page
from Locators.DashboardLocators import *
from Locators.SettingsLocators import *
import time
from Config.Users import *


class SettingsPage(Page):

    def check_email_is_not_verified(self, email):
        """
        Проверяет что email не подтвержден со страницы dashboard
        time.sleep(2) потому что после регистрации емейл в settings подтягивается не сразу
        :param email: email пользователя
        """
        current_email = ''
        while current_email == '':
            self.wait_and_click(NavigationButtons.settings)
            time.sleep(0.5)
            self.wait_and_click(NavigationLinks.account)
            current_email = self.get_element_attribute(Account.emailNotifications, "value")
        assert email == current_email
        self.wait_and_assert_element_text(Account.dangerText, "Verify email")

    def check_email_is_verified(self, email):
        """
        Проверяет что после перехода по ссылке email подтвержден со страницы dashboard
        :param email: email пользователя
        """
        self.wait_and_click(NavigationButtons.settings)
        self.wait_and_click(NavigationLinks.account)
        current_email = self.get_element_attribute(Account.emailNotifications, "value")
        assert email == current_email
        self.wait_and_assert_element_text(Account.successText, "Email is verified.")

