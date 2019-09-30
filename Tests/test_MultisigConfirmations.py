import pytest
from Pages.LoginPage import *
from Pages.SettingsPage import *
from Pages.TransactionsPage import *
from Pages.SecurityPage import *
from Config.Users import *
from Helpers.SQLHelper import *
from Helpers.SMTPHelper import *
from xrayplugin.plugin import xray

sql = SQLHelper()
email = SMTPHelper()


@pytest.fixture(scope='function')
def data_basic_user(driver):
    loginPage = LoginPage(driver)
    loginPage.login_as_basic_user(ExistingBasicVerifiedUser.email, ExistingBasicVerifiedUser.password)
    loginPage.input_pincode_login(ExistingBasicVerifiedUser.pincode)
    sql.delete_multisig_emails(ExistingBasicVerifiedUser.email)
    yield


@pytest.fixture(scope='function')
def data_google_user(driver):
    email.delete_emails_from_gmail(ExistingBasicUser.email, ExistingBasicUser.password, "Freewallet", "Verify your multisig email")
    sql.delete_multisig_emails(MultisigGoogleUser.email)
    loginPage = LoginPage(driver)
    loginPage.clear_google_cookies()
    loginPage.login_as_google_user(MultisigGoogleUser.email, MultisigGoogleUser.password)
    loginPage.input_pincode_login(MultisigGoogleUser.pincode)
    yield
    email.delete_emails_from_gmail(ExistingBasicUser.email, ExistingBasicUser.password, "Freewallet", "Verify your multisig email")
    sql.delete_multisig_emails(MultisigGoogleUser.email)

@pytest.fixture(scope='function')
def disable_multisig(driver):
    email.delete_emails_from_gmail(ExistingBasicUser.email, ExistingBasicUser.password, "Freewallet", "Verify removing your confirmation email")
    sql.delete_multisig_emails(MultisigGoogleUser.email)
    sql.add_multisig_email(MultisigGoogleUser.email, ExistingBasicUser.email)
    loginPage = LoginPage(driver)
    loginPage.clear_google_cookies()
    loginPage.login_as_google_user(MultisigGoogleUser.email, MultisigGoogleUser.password)
    loginPage.input_pincode_login(MultisigGoogleUser.pincode)
    yield
    email.delete_emails_from_gmail(ExistingBasicUser.email, ExistingBasicUser.password, "Freewallet", "Verify removing your confirmation email")
    sql.delete_multisig_emails(MultisigGoogleUser.email)

@pytest.fixture(scope='function')
def existing_multisig(driver):
    sql.delete_multisig_emails(MultisigGoogleUser.email)
    sql.add_multisig_email(MultisigGoogleUser.email, ExistingBasicUser.email)
    loginPage = LoginPage(driver)
    loginPage.clear_google_cookies()
    loginPage.login_as_google_user(MultisigGoogleUser.email, MultisigGoogleUser.password)
    loginPage.input_pincode_login(MultisigGoogleUser.pincode)
    yield
    sql.delete_multisig_emails(MultisigGoogleUser.email)


class TestClass:

    @pytest.mark.usefixtures("data_basic_user")
    def test_MultisigEmailDiscard(self, driver):
        securityPage = SecurityPage(driver)
        securityPage.navigate_to_email_confirmation()
        securityPage.add_multisig_address(ExistingBasicUser.email)
        securityPage.discard_multisig_address()

    @pytest.mark.usefixtures("data_google_user")
    @xray("QA-814")
    @pytest.mark.websmoke
    def test_EnableMultisigConfirmation(self, driver):
        securityPage = SecurityPage(driver)
        loginPage = LoginPage(driver)
        securityPage.navigate_to_email_confirmation()
        securityPage.add_multisig_address(ExistingBasicUser.email)
        link = email.get_multisig_link_from_email(ExistingBasicUser.email, ExistingBasicUser.password, "Freewallet", "Verify your multisig email")
        securityPage.navigate_to_link(link)
        loginPage.input_pincode_login(MultisigGoogleUser.pincode)
        securityPage.navigate_to_email_confirmation()
        securityPage.wait_until_element_visible(Multisig.confirmedAddressFirst)
        securityPage.wait_and_assert_element_text(Multisig.confirmedAddressFirst, ExistingBasicUser.email)

    @pytest.mark.usefixtures("disable_multisig")
    @xray("QA-815")
    def test_DisableMultisigConfirmation(self, driver):
        securityPage = SecurityPage(driver)
        loginPage = LoginPage(driver)
        securityPage.navigate_to_email_confirmation()
        securityPage.disable_multisig()
        link = email.get_multisig_link_from_email(ExistingBasicUser.email, ExistingBasicUser.password, "Freewallet", "Verify removing your confirmation email")
        securityPage.navigate_to_link(link)
        loginPage.input_pincode_login(MultisigGoogleUser.pincode)
        securityPage.navigate_to_email_confirmation()
        securityPage.wait_and_assert_element_text(Multisig.email1, '')


    @pytest.mark.usefixtures("existing_multisig")
    @xray("QA-766")
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


