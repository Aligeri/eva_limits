import pytest
from Pages.LoginPage import *
from Pages.SettingsPage import *
from Pages.TransactionsPage import *
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
    sql.delete_multisig_emails(ExistingBasicVerifiedUser.email)
    yield



@pytest.fixture(scope='function')
@pytest.mark.usefixtures("driver")
def data_google_user(driver):
    sql = SQLHelper()
    email = SMTPHelper()
    email.delete_emails_from_gmail(ExistingBasicUser.email, ExistingBasicUser.password)
    sql.delete_multisig_emails(MultisigGoogleUser.email)
    loginPage = LoginPage(driver)
    loginPage.reset_session()
    loginPage.clear_google_cookies()
    loginPage.login_as_google_user(MultisigGoogleUser.email, MultisigGoogleUser.password)
    loginPage.input_pincode_login(MultisigGoogleUser.pincode)
    yield
    email.delete_emails_from_gmail(ExistingBasicUser.email, ExistingBasicUser.password)
    sql.delete_multisig_emails(MultisigGoogleUser.email)

@pytest.fixture(scope='function')
@pytest.mark.usefixtures("driver")
def disable_multisig(driver):
    sql = SQLHelper()
    email = SMTPHelper()
    email.delete_emails_from_gmail(ExistingBasicUser.email, ExistingBasicUser.password)
    sql.delete_multisig_emails(MultisigGoogleUser.email)
    sql.add_multisig_email(MultisigGoogleUser.email, ExistingBasicUser.email)
    loginPage = LoginPage(driver)
    loginPage.reset_session()
    loginPage.clear_google_cookies()
    loginPage.login_as_google_user(MultisigGoogleUser.email, MultisigGoogleUser.password)
    loginPage.input_pincode_login(MultisigGoogleUser.pincode)
    yield
    email.delete_emails_from_gmail(ExistingBasicUser.email, ExistingBasicUser.password)
    sql.delete_multisig_emails(MultisigGoogleUser.email)

@pytest.fixture(scope='function')
@pytest.mark.usefixtures("driver")
def existing_multisig(driver):
    sql = SQLHelper()
    #sql.delete_multisig_emails(MultisigGoogleUser.email)
    #sql.add_multisig_email(MultisigGoogleUser.email, ExistingBasicUser.email)
    loginPage = LoginPage(driver)
    loginPage.reset_session()
    loginPage.clear_google_cookies()
    loginPage.login_as_google_user(MultisigGoogleUser.email, MultisigGoogleUser.password)
    loginPage.input_pincode_login(MultisigGoogleUser.pincode)
    yield
    #sql.delete_multisig_emails(MultisigGoogleUser.email)

@pytest.mark.usefixtures("driver")
class TestClass:

    @pytest.mark.usefixtures("data_basic_user")
    def test_MultisigEmailDiscard(self, driver):
        securityPage = SecurityPage(driver)
        securityPage.navigate_to_email_confirmation()
        securityPage.add_multisig_address(ExistingBasicUser.email)
        securityPage.discard_multisig_address()

    @pytest.mark.usefixtures("data_google_user")
    def test_EnableMultisigConfirmation(self, driver):
        securityPage = SecurityPage(driver)
        loginPage = LoginPage(driver)
        smtp = SMTPHelper()
        securityPage.navigate_to_email_confirmation()
        securityPage.add_multisig_address(ExistingBasicUser.email)
        link = smtp.get_multisig_link_from_email(ExistingBasicUser.email, ExistingBasicUser.password, "Freewallet", "Verify your multisig email")
        securityPage.navigate_to_link(link)
        loginPage.input_pincode_login(MultisigGoogleUser.pincode)
        securityPage.navigate_to_email_confirmation()
        securityPage.wait_until_element_visible(Multisig.confirmedAddressFirst)
        securityPage.wait_and_assert_element_text(Multisig.confirmedAddressFirst, ExistingBasicUser.email)

    @pytest.mark.usefixtures("disable_multisig")
    def test_DisableMultisigConfirmation(self, driver):
        securityPage = SecurityPage(driver)
        loginPage = LoginPage(driver)
        smtp = SMTPHelper()
        securityPage.navigate_to_email_confirmation()
        securityPage.disable_multisig()
        link = smtp.get_multisig_link_from_email(ExistingBasicUser.email, ExistingBasicUser.password, "Freewallet", "Verify removing your confirmation email")
        securityPage.navigate_to_link(link)
        loginPage.input_pincode_login(MultisigGoogleUser.pincode)
        securityPage.navigate_to_email_confirmation()
        securityPage.wait_and_assert_element_text(Multisig.email1, '')


    #@pytest.mark.skip("Опять емейлы")
    @pytest.mark.usefixtures("existing_multisig")
    def test_CancelMultisigTransaction(self, driver):
        transactionsPage = TransactionsPage(driver)
        comment = str(time.time())
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_user_id("BTC")
        transactionsPage.send_transaction_step_2_user_id(ExistingBasicUser.userID)
        transactionsPage.send_transaction_step_3("0.00000001")
        transactionsPage.send_transaction_step_4(comment)
        transactionsPage.check_unconfirmed_transaction(comment)
        transactionsPage.cancel_transaction()
        transactionsPage.check_canceled_transaction(comment, "Email confirmation canceled by user")


