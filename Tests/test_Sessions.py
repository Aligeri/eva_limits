import pytest
from Pages.LoginPage import *
from Pages.SettingsPage import *
from Pages.TransactionsPage import *
from Config.Users import *
from Helpers.SQLHelper import *
from Helpers.SMTPHelper import *
from Locators.SecurityLocators import *
from xrayplugin.plugin import xray


email = SMTPHelper()


@pytest.fixture(scope="function")
def data_892():
    email.delete_emails_from_gmail(ExistingBasicUser2.email, ExistingBasicUser2.password, "Freewallet", "Login attempt to your Freewallet account")
    yield
    email.delete_emails_from_gmail(ExistingBasicUser2.email, ExistingBasicUser2.password, "Freewallet", "Login attempt to your Freewallet account")


class TestClass:

    @xray("QA-826", "QA-892", "QA-691")
    @pytest.mark.usefixtures("data_892")
    @pytest.mark.websmoke
    def test_drop_session_from_email(self, driver):
        loginPage = LoginPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser2.email, ExistingBasicUser2.password)
        loginPage.input_pincode_login(ExistingBasicUser2.pincode)
        link = email.get_session_drop_link_from_email(ExistingBasicUser2.email, ExistingBasicUser2.password, "Freewallet", "Login attempt to your Freewallet account")
        loginPage.navigate_to_link(link)
        loginPage.login_as_basic_user(ExistingBasicUser2.email, ExistingBasicUser2.password)
        loginPage.input_pincode_login(ExistingBasicUser2.pincode)
        loginPage.wait_and_assert_element_text(DashboardLocators.userName, ExistingBasicUser2.userName)
