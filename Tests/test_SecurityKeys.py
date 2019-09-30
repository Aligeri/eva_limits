import pytest
from Pages.LoginPage import *
from Pages.SettingsPage import *
from Pages.TransactionsPage import *
from Config.Users import *
from Helpers.SQLHelper import *
from Locators.SecurityLocators import *
from xrayplugin.plugin import xray

"""
@pytest.fixture(scope="function")
def data_1037():
    sql = SQLHelper()
    sql.delete_limits_by_email_from_database(ExistingBasicUser.email1037)
    yield
    sql.delete_limits_by_email_from_database(ExistingBasicUser.email1037)
"""

class TestClass:

    @xray("QA-1085")
    def test_generate_mnemonic_key(self, driver):
        loginPage = LoginPage(driver)
        settings_page = SettingsPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email1085, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        settings_page.check_email_is_loaded(ExistingBasicUser.email1085)
        settings_page.navigate_to_export_wallet()
        settings_page.navigate_to_mnemonic()
        settings_page.wait_and_click(Mnemonic.gotIt)
        settings_page.wait_and_click(Mnemonic.generate)
        settings_page.generate_wallet_key()
        settings_page.wait_and_click(Mnemonic.continueButton)
        text = settings_page.get_element_text(Mnemonic.mnemonicKey)
        list = text.split(" ")
        settings_page.wait_and_click(Mnemonic.continueButton)
        settings_page.select_mnemonic_words(list)
        settings_page.wait_and_click(Mnemonic.continueButton)
        settings_page.wait_and_input_text(Mnemonic.thirdWordInput, list[2])
        settings_page.wait_to_be_clickable(Mnemonic.finishButton)

    @xray("QA-1086")
    def test_generate_private_key(self, driver):
        loginPage = LoginPage(driver)
        settings_page = SettingsPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email1085, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        settings_page.check_email_is_loaded(ExistingBasicUser.email1085)
        settings_page.navigate_to_export_wallet()
        settings_page.navigate_to_private_key()
        settings_page.wait_and_click(Mnemonic.gotIt)
        settings_page.wait_and_click(Mnemonic.generate)
        settings_page.generate_wallet_key()
        settings_page.wait_and_click(Mnemonic.continueButton)
        privateKey = settings_page.get_element_text(Mnemonic.privateKey)
        assert privateKey is not None
        publicKey = settings_page.get_element_text(Mnemonic.publicKey)
        assert publicKey is not None
        settings_page.wait_and_click(Mnemonic.storedCheckbox)
        settings_page.wait_to_be_clickable(Mnemonic.continueButton)