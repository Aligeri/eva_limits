import pytest
from Pages.LoginPage import *
from Pages.SettingsPage import *
from Pages.SecurityPage import *
from Pages.TransactionsPage import *
from Config.Users import *
from Helpers.SQLHelper import *
from Helpers.SMTPHelper import *
from Locators.SecurityLocators import *
from xrayplugin.plugin import xray


email = SMTPHelper()
sql = SQLHelper()

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

    @xray("QA-828")
    @pytest.mark.websmoke
    def test_other_sessions_displayed(self, driver):
        loginPage = LoginPage(driver)
        securityPage = SecurityPage(driver)
        sql.delete_sessions_by_email(ExistingBasicUser.email_829)
        sql.insert_session(ExistingBasicUser.email_829, "Another session")
        sql.insert_session(ExistingBasicUser.email_829, "Yet another session")
        loginPage.login_as_basic_user(ExistingBasicUser.email_829, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        securityPage.navigate_to_security()
        securityPage.navigate_to_active_sessions()
        sessions_count = securityPage.get_current_sessions_count()
        assert sessions_count == 3
        securityPage.find_session_by_model("Web, Another session")
        securityPage.find_session_by_model("Web, Yet another session")

    @xray("QA-828")
    @pytest.mark.websmoke
    def test_drop_single_session(self, driver):
        loginPage = LoginPage(driver)
        securityPage = SecurityPage(driver)
        sql.delete_sessions_by_email(ExistingBasicUser.email_828)
        sql.insert_session(ExistingBasicUser.email_828, "Drop single session test")
        loginPage.login_as_basic_user(ExistingBasicUser.email_828, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        securityPage.navigate_to_security()
        securityPage.navigate_to_active_sessions()
        count_before = securityPage.get_current_sessions_count()
        assert count_before == 2
        securityPage.drop_session_by_model("Web, Drop single session test")
        db_count = len(sql.get_deleted_sessions_by_email(ExistingBasicUser.email_828))
        count_after = securityPage.get_current_sessions_count()
        assert count_after == 1
        assert db_count == 1

    @xray("QA-827")
    @pytest.mark.websmoke
    def test_drop_all_sessions(self, driver):
        loginPage = LoginPage(driver)
        securityPage = SecurityPage(driver)
        sql.delete_sessions_by_email(ExistingBasicUser.email_827)
        sql.insert_session(ExistingBasicUser.email_827, "Drop multiple sessions test 1")
        sql.insert_session(ExistingBasicUser.email_827, "Drop multiple sessions test 2")
        sql.insert_session(ExistingBasicUser.email_827, "Drop multiple sessions test 3")
        loginPage.login_as_basic_user(ExistingBasicUser.email_827, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        securityPage.navigate_to_security()
        securityPage.navigate_to_active_sessions()
        count_before = securityPage.get_current_sessions_count()
        assert count_before == 4
        securityPage.drop_all_sessions()
        db_count = len(sql.get_deleted_sessions_by_email(ExistingBasicUser.email_827))
        count_after = securityPage.get_current_sessions_count()
        assert count_after == 1
        assert db_count == 3




