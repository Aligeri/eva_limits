from Pages.BasePage import Page
from Locators.DashboardLocators import *
from Locators.SettingsLocators import *
import time
from Config.Users import *


class SettingsPage(Page):

    def navigate_to_account(self):
        self.wait_and_click(NavigationLinks.account)

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

    def change_fiat_currency(self, currency):
        """
        Меняет local currency со страницы settings
        :param currency: валюта на которую поменяется local currency, usd/eur/gbp/rub
        :return:
        """
        CURRENCY = {
            "usd": FiatCurrency.fiatUsd,
            "eur": FiatCurrency.fiatEur,
            "gbp": FiatCurrency.fiatGbp,
            "rub": FiatCurrency.fiatRub,
        }
        self.navigate_to_account()
        self.wait_and_click(FiatCurrency.fiatCurrencyDropdown)
        self.wait_and_click(CURRENCY[currency])

    def change_name(self, name):
        """""
        Меняет имя пользователя на вкладке UserDetails
        """""
        self.wait_until_element_visible(Identity.Badge)
        self.wait_and_input_text(userDetails.Name, name)
        self.wait_and_click(userDetails.SaveBtn)