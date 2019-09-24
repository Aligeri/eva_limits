import pytest
from Pages.LoginPage import *
from Pages.SecurityPage import *
from Pages.TransactionsPage import *
from Config.Users import *
from Helpers.SQLHelper import *
from Locators.SecurityLocators import *
from xrayplugin.plugin import xray


sql = SQLHelper()


@pytest.fixture(scope="function")
def data_1034():
    sql.delete_limits_by_email_from_database(ExistingBasicUser.email)
    yield
    sql.delete_limits_by_email_from_database(ExistingBasicUser.email)


@pytest.fixture(scope="function")
def data_837():
    sql.delete_limits_by_email_from_database(ExistingBasicUser.email837)
    yield
    sql.delete_limits_by_email_from_database(ExistingBasicUser.email837)


@pytest.fixture(scope="function")
def data_1037():
    sql.delete_limits_by_email_from_database(ExistingBasicUser.email1037)
    yield
    sql.delete_limits_by_email_from_database(ExistingBasicUser.email1037)


class TestClass:

    @xray("QA-954", "QA-713")
    @pytest.mark.smoke
    def test_change_pincode(self, driver):
        loginPage = LoginPage(driver)
        securityPage = SecurityPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email954, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        securityPage.navigate_to_pincode()
        securityPage.input_security_pincode_current(ExistingBasicUser.pincode)
        securityPage.input_security_pincode_new(ExistingBasicUser.changedPincode)
        securityPage.input_security_pincode_repeat(ExistingBasicUser.changedPincode)
        securityPage.wait_until_element_visible(SecurityPincode.successPopup)
        securityPage.refresh_page()
        loginPage.input_pincode_login(ExistingBasicUser.changedPincode)
        securityPage.input_security_pincode_current(ExistingBasicUser.changedPincode)
        securityPage.input_security_pincode_new(ExistingBasicUser.pincode)
        securityPage.input_security_pincode_repeat(ExistingBasicUser.pincode)
        securityPage.wait_until_element_visible(SecurityPincode.successPopup)

    @xray("QA-837", "QA-838")
    @pytest.mark.usefixtures("data_837")
    @pytest.mark.smoke
    def test_add_and_change_limit(self, driver):
        loginPage = LoginPage(driver)
        securityPage = SecurityPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email837, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        securityPage.navigate_to_limits()
        securityPage.create_new_weekly_limit("FWH", "100")
        securityPage.close_limit_modal()
        securityPage.change_limit_after_creation("200", "FWH")
        securityPage.close_limit_modal()
        securityPage.check_limit_buttons_are_not_displayed("FWH")

    @xray("QA-1037")
    @pytest.mark.smoke
    @pytest.mark.usefixtures("data_1037")
    def test_add_and_disable_limit(self, driver):
        loginPage = LoginPage(driver)
        securityPage = SecurityPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email1037, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        securityPage.navigate_to_limits()
        securityPage.create_new_weekly_limit("BTC", 100)
        securityPage.close_limit_modal()
        securityPage.disable_limit_after_creation("BTC")
        securityPage.close_limit_modal()
        securityPage.check_limit_buttons_are_not_displayed("BTC")

    @xray("QA-1034")
    @pytest.mark.usefixtures("data_1034")
    @pytest.mark.smoke
    def test_add_and_spend_limit(self, driver):
        transactionsPage = TransactionsPage(driver)
        loginPage = LoginPage(driver)
        securityPage = SecurityPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        comment = str(time.time())
        securityPage.navigate_to_limits()
        securityPage.create_new_weekly_limit("BTC", "0.00000001")
        securityPage.close_limit_modal()
        securityPage.check_BTC_limit_percent("100%")
        securityPage.navigate_to_dashboard()
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_to_user_id("BTC", "0.00000001", ExistingGoogleUser.userID, comment)
        transactionsPage.wait_until_element_visible(Send.firstTransactionAmount)
        transactionsPage.navigate_to_send()
        loginPage.refresh_page()
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        transactionsPage.check_limit_exceeded_transaction("BTC", "0.00000001", ExistingGoogleUser.userID)
        securityPage.navigate_to_limits()
        securityPage.check_BTC_limit_percent("0%")
