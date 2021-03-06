from Pages.BasePage import Page
from Locators.DashboardLocators import *
from Locators.SettingsLocators import *
import time
from Config.Users import *

LANGUAGE = {
    "en": Account.languageEn,
    "ja": Account.languageJa,
    "ru": Account.languageRu,
}

IDENTITY_FIELDS = {
    "firstName": Identity.firstName,
    "secondName": Identity.secondName,
    "birthDate": Identity.birthDate,
    "identityFrontFile": Identity.identityFrontFile,
    "identityBackFile": Identity.identityBackFile,
    "selfieFile": Identity.selfieFile
}

IDENTITY_ERRORS = {
    "firstName": Identity.firstNameError,
    "secondName": Identity.secondNameError,
    "birthDate": Identity.birthDateError,
    "identityFrontFile": Identity.identityFrontFileError,
    "identityBackFile": Identity.identityBackFileError,
    "selfieFile": Identity.selfieFileError
}

IDENTITY_FILENAMES = {
    "identityFrontFile": Identity.identityFrontFileName,
    "identityBackFile": Identity.identityBackFileName,
    "selfieFile": Identity.selfieFileName
}

class SettingsPage(Page):


    def navigate_to_account(self):
        self.wait_and_click(NavigationLinks.account)

    def navigate_to_export_wallet(self):
        self.wait_and_click(NavigationButtons.settings)
        self.wait_and_click(NavigationLinks.exportWallet)

    def navigate_to_import_wallet(self):
        self.wait_and_click(NavigationButtons.settings)
        self.wait_and_click(NavigationLinks.importWallet)

    def navigate_to_mnemonic(self):
        self.wait_and_click(NavigationLinks.mnemonic)

    def navigate_to_private_key(self):
        self.wait_and_click(NavigationLinks.privateKey)

    def generate_wallet_key(self):
        while self.get_element_text(Mnemonic.percent) != "100%":
            self.move_mouse_in_element(Mnemonic.mouseArea)

    def navigate_to_identity(self):
        self.wait_and_click(NavigationButtons.settings)
        self.wait_and_click(NavigationLinks.identity)

    def select_mnemonic_words(self, list):
        for word in list:
            self.wait_and_click((By.XPATH, "//div[@class='mnemonic__mmTag--2T4CD' and text()='%s']" % word))


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

    def check_email_is_loaded(self, email):
        """
        Проверяет что email не подтвержден со страницы dashboard
        time.sleep(2) потому что после регистрации емейл в settings подтягивается не сразу
        :param email: email пользователя
        """
        current_email = ''
        while current_email == '':
            self.wait_and_click(NavigationButtons.settings)
            time.sleep(1)
            self.wait_and_click(NavigationLinks.account)
            current_email = self.get_element_attribute(Account.emailNotifications, "value")
        assert email == current_email

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
        self.clear_input_text(userDetails.Name)
        self.wait_and_input_text(userDetails.Name, name)
        self.wait_and_click(userDetails.SaveBtn)

    def change_user_id(self, new_id):
        """""
        Меняет user id на вкладке UserDetails
        """""
        self.wait_until_element_visible(Identity.Badge)
        self.clear_input_text(userDetails.UserId)
        self.wait_and_input_text(userDetails.UserId, new_id)
        self.wait_and_click(userDetails.SaveBtn)

    def change_email(self, new_email):
        """""
        Меняет email на вкладке Account
        """""
        self.wait_until_element_visible(Identity.Badge)
        self.clear_input_text(Account.emailNotifications)
        self.wait_and_input_text(Account.emailNotifications, new_email)
        self.wait_and_click(Account.SaveBtn)
        self.wait_until_element_visible(Account.VerificationPopup)
        self.wait_and_click(Account.SendLinkBtn)
        self.wait_until_element_visible(Account.ConfirmEmailText)

    def select_language_in_settings(self, language):
        #self.hover_over_element(LanguageSelectors.dropdown)
        self.wait_and_click(Account.languageDropdown)
        self.wait_and_click(LANGUAGE[language])

    def check_identity_errors(self, field, value, error):
        self.wait_and_input_text(IDENTITY_FIELDS[field], value)
        self.wait_and_click(NavigationLinks.identity)
        self.assert_element_text(IDENTITY_ERRORS[field], error)

    def check_identity_errors_file_upload(self, field, value, error):
        self.upload_file(IDENTITY_FIELDS[field], value)
        self.assert_element_text(IDENTITY_ERRORS[field], error)

    def assert_identity_error_not_displayed(self, field, value):
        self.wait_and_input_text(IDENTITY_FIELDS[field], value)
        self.wait_and_click(NavigationLinks.identity)
        self.wait_until_element_invisible(IDENTITY_ERRORS[field], 1)

    def check_identity_error_not_displayed_file_upload(self, field, value):
        self.upload_file(IDENTITY_FIELDS[field], value)
        self.wait_until_element_visible(IDENTITY_FILENAMES[field])
        self.wait_until_element_invisible(IDENTITY_ERRORS[field], 1)

    def send_file(self, field, value):
        a = self.driver.find_element(*IDENTITY_FIELDS[field])
        a.send_keys(value)
    def resend_link(self):
        self.wait_and_click(Account.ResendLink)
