import pytest
from Pages.LoginPage import *
from Pages.SettingsPage import *
from Pages.SecurityPage import *
from Config.Users import *
from Helpers.SQLHelper import *
from Helpers.SMTPHelper import *


@pytest.fixture(scope='function')
@pytest.mark.usefixtures("driver")
def data_basic_user(driver):
    sql = SQLHelper()
    loginPage = LoginPage(driver)
    loginPage.reset_session()
    loginPage.login_as_basic_user(ExistingBasicVerifiedUser.email, ExistingBasicVerifiedUser.password)
    loginPage.input_pincode_login(ExistingBasicVerifiedUser.pincode)
    yield
    sql.delete_multisig_emails(ExistingBasicVerifiedUser.email)


@pytest.fixture(scope='function')
def data_google_user(driver):
    sql = SQLHelper()
    loginPage = LoginPage(driver)
    loginPage.reset_session()
    loginPage.navigate_to_signup_page()
    loginPage.login_as_google_user(MultisigGoogleUser.email, MultisigGoogleUser.password)
    loginPage.input_pincode_create(MultisigGoogleUser.pincode)
    loginPage.input_pincode_repeat(MultisigGoogleUser.pincode)
    yield
    sql.delete_multisig_emails(MultisigGoogleUser.email)
    sql.delete_user_from_database(MultisigGoogleUser.email)


@pytest.mark.usefixtures("driver")
class TestClass:

    @pytest.mark.usefixtures("data_basic_user")
    def test_MultisigEmailDiscard(self, driver):
        securityPage = SecurityPage(driver)
        securityPage.navigate_to_email_confirmation()
        securityPage.add_multisig_address(ExistingBasicUser.email)
        securityPage.discard_multisig_address()

    @pytest.mark.skip("Опять емейлы")
    @pytest.mark.usefixtures("data_google_user")
    def test_MultisigEmailConfirm(self, driver):
        smtp = SMTPHelper()
        securityPage = SecurityPage(driver)
        loginPage = LoginPage(driver)
        loginPage.clear_google_cookies()
        securityPage.navigate_to_email_confirmation()
        securityPage.add_multisig_address(ExistingBasicUser.email)
        link = smtp.get_multisig_link_from_email(ExistingBasicUser.email, ExistingBasicUser.password, "Freewallet", "Verify your multisig email")
        securityPage.navigate_to_link(link)
        loginPage.input_pincode_login(MultisigGoogleUser.pincode)


