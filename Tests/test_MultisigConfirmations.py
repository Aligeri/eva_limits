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
    loginPage.login_as_google_user(MultisigGoogleUser.email, MultisigGoogleUser.password, MultisigGoogleUser.otp_code)
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
    loginPage.login_as_google_user(MultisigGoogleUser.email, MultisigGoogleUser.password, MultisigGoogleUser.otp_code)
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
    loginPage.login_as_google_user(MultisigGoogleUser.email, MultisigGoogleUser.password, MultisigGoogleUser.otp_code)
    loginPage.input_pincode_login(MultisigGoogleUser.pincode)
    yield
    sql.delete_multisig_emails(MultisigGoogleUser.email)

@pytest.fixture(scope='function')
def preset_for_add_second_multisig(driver):
    email.delete_emails_from_gmail(UserforAddSecondMultisig.first_multisig_email, UserforAddSecondMultisig.email_password, "Freewallet", "Verify your multisig email")
    email.delete_emails_from_gmail(UserforAddSecondMultisig.second_multisig_email, UserforAddSecondMultisig.email_password, "Freewallet", "Verify your multisig email")
    email.delete_emails_from_gmail(UserforAddSecondMultisig.first_multisig_email, UserforAddSecondMultisig.email_password, "Freewallet", "Verify add new confirmation email")
    sql.delete_multisig_emails(UserforAddSecondMultisig.email)
    sql.add_multisig_email(UserforAddSecondMultisig.email, UserforAddSecondMultisig.first_multisig_email)
    yield
    email.delete_emails_from_gmail(UserforMultisigTransaction.first_multisig_email, UserforMultisigTransaction.email_password, "Freewallet", "Verify transaction")
    email.delete_emails_from_gmail(UserforMultisigTransaction.second_multisig_email, UserforMultisigTransaction.email_password, "Freewallet", "Verify transaction")
    sql.delete_multisig_emails(UserforAddSecondMultisig.email)

@pytest.fixture(scope='function')
def preset_for_multisig_transaction(driver):
    email.delete_emails_from_gmail(UserforMultisigTransaction.first_multisig_email, UserforMultisigTransaction.email_password, "Freewallet", "Verify transaction")
    email.delete_emails_from_gmail(UserforMultisigTransaction.second_multisig_email, UserforMultisigTransaction.email_password, "Freewallet", "Verify transaction")
    sql.delete_multisig_emails(UserforMultisigTransaction.email)
    sql.add_multisig_email(UserforMultisigTransaction.email, UserforMultisigTransaction.first_multisig_email)
    sql.add_multisig_email(UserforMultisigTransaction.email, UserforMultisigTransaction.second_multisig_email)
    yield
    email.delete_emails_from_gmail(UserforMultisigTransaction.first_multisig_email, UserforMultisigTransaction.email_password, "Freewallet", "Verify transaction")
    email.delete_emails_from_gmail(UserforMultisigTransaction.second_multisig_email, UserforMultisigTransaction.email_password, "Freewallet", "Verify transaction")
    sql.delete_multisig_emails(UserforMultisigTransaction.email)

@pytest.fixture(scope='function')
def preset_for_disable_multisig(driver):
    email.delete_emails_from_gmail(UserforDisableMultisig.first_multisig_email, UserforDisableMultisig.email_password, "Freewallet", "Verify removing your confirmation email")
    email.delete_emails_from_gmail(UserforDisableMultisig.second_multisig_email, UserforDisableMultisig.email_password, "Freewallet", "Verify removing your confirmation email")
    sql.delete_multisig_emails(UserforDisableMultisig.email)
    sql.add_multisig_email(UserforDisableMultisig.email, UserforDisableMultisig.first_multisig_email)
    sql.add_multisig_email(UserforDisableMultisig.email, UserforDisableMultisig.second_multisig_email)
    yield
    email.delete_emails_from_gmail(UserforDisableMultisig.first_multisig_email, UserforDisableMultisig.email_password, "Freewallet", "Verify removing your confirmation email")
    email.delete_emails_from_gmail(UserforDisableMultisig.second_multisig_email, UserforDisableMultisig.email_password, "Freewallet", "Verify removing your confirmation email")
    sql.delete_multisig_emails(UserforDisableMultisig.email)

@pytest.fixture(scope='function')
def preset_for_delete_one_multisig_address(driver):
    email.delete_emails_from_gmail(UserforDeleteOneMultisigAddress.first_multisig_email, UserforDeleteOneMultisigAddress.email_password, "Freewallet", "Verify removing your confirmation email")
    email.delete_emails_from_gmail(UserforDeleteOneMultisigAddress.second_multisig_email, UserforDeleteOneMultisigAddress.email_password, "Freewallet", "Verify removing your confirmation email")
    sql.delete_multisig_emails(UserforDeleteOneMultisigAddress.email)
    sql.add_multisig_email(UserforDeleteOneMultisigAddress.email, UserforDeleteOneMultisigAddress.first_multisig_email)
    sql.add_multisig_email(UserforDeleteOneMultisigAddress.email, UserforDeleteOneMultisigAddress.second_multisig_email)
    yield
    email.delete_emails_from_gmail(UserforDeleteOneMultisigAddress.first_multisig_email, UserforDeleteOneMultisigAddress.email_password, "Freewallet", "Verify removing your confirmation email")
    email.delete_emails_from_gmail(UserforDeleteOneMultisigAddress.second_multisig_email, UserforDeleteOneMultisigAddress.email_password, "Freewallet", "Verify removing your confirmation email")
    sql.delete_multisig_emails(UserforDeleteOneMultisigAddress.email)

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
        link = email.get_multisig_remove_link_from_email(ExistingBasicUser.email, ExistingBasicUser.password, "Freewallet", "Verify removing your confirmation email")
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

    @pytest.mark.usefixtures("preset_for_add_second_multisig")
    @xray("QA-816")
    @pytest.mark.websmoke
    def test_add_second_multisig(self, driver):
        loginPage = LoginPage(driver)
        loginPage.reset_session()
        loginPage.login_as_basic_user(UserforAddSecondMultisig.email, UserforAddSecondMultisig.password)
        loginPage.input_pincode_login(UserforAddSecondMultisig.pincode)
        securityPage = SecurityPage(driver)
        securityPage.navigate_to_email_confirmation()
        securityPage.add_second_multisig_address(UserforAddSecondMultisig.second_multisig_email)
        link = email.get_multisig_link_from_email(UserforAddSecondMultisig.second_multisig_email, UserforAddSecondMultisig.email_password, "Freewallet","Verify your multisig email")
        securityPage.navigate_to_link(link)
        loginPage.input_pincode_login(UserforAddSecondMultisig.pincode)
        securityPage.navigate_to_email_confirmation()
        securityPage.wait_and_assert_element_text(Multisig.pending_multisig_status,"Waiting for confirmation (1/2)")
        link1 = email.get_add_multisig_link_from_email(UserforAddSecondMultisig.first_multisig_email, UserforAddSecondMultisig.email_password, "Freewallet","Verify add new confirmation email")
        securityPage.navigate_to_link(link1)
        loginPage.input_pincode_login(UserforAddSecondMultisig.pincode)
        securityPage.navigate_to_email_confirmation()
        securityPage.wait_and_assert_element_text(Multisig.disclaimer_title,"Active")
        securityPage.check_veified_multisig_addreses(UserforAddSecondMultisig.first_multisig_email, UserforAddSecondMultisig.second_multisig_email)

    @pytest.mark.usefixtures("preset_for_multisig_transaction")
    @xray("QA-762")
    @pytest.mark.websmoke
    def test_multisig_transaction_with_2_emails(self, driver):
        loginPage = LoginPage(driver)
        loginPage.reset_session()
        loginPage.login_as_basic_user(UserforMultisigTransaction.email, UserforMultisigTransaction.password)
        loginPage.input_pincode_login(UserforMultisigTransaction.pincode)
        comment = str(time.time())
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_to_user_id('DOGE','0.1',RichUser.email,comment)
        transactionsPage.check_unconfirmed_transaction_by_comment(comment)
        link = email.get_multisig_transaction_link_from_email(UserforMultisigTransaction.first_multisig_email, UserforMultisigTransaction.email_password, "Freewallet", "Verify transaction")
        transactionsPage.navigate_to_link(link)
        link1 = email.get_multisig_transaction_link_from_email(UserforMultisigTransaction.second_multisig_email, UserforMultisigTransaction.email_password, "Freewallet", "Verify transaction")
        transactionsPage.navigate_to_link(link1)
        loginPage.input_pincode_login(UserforAddSecondMultisig.pincode)
        transactionsPage.check_completed_transaction(comment)

    @pytest.mark.usefixtures("preset_for_disable_multisig")
    @xray("QA-899")
    @pytest.mark.websmoke
    def test_disable_multisig_for_2_emails(self, driver):
        loginPage = LoginPage(driver)
        loginPage.reset_session()
        loginPage.login_as_basic_user(UserforDisableMultisig.email, UserforMultisigTransaction.password)
        loginPage.input_pincode_login(UserforDisableMultisig.pincode)
        securityPage = SecurityPage(driver)
        securityPage.navigate_to_email_confirmation()
        securityPage.disable_multisig()
        link = email.get_disable_multisig_link_from_email(UserforDisableMultisig.first_multisig_email, UserforDisableMultisig.email_password, "Freewallet", "Verify removing your confirmation email")
        securityPage.navigate_to_link(link)
        link1 = email.get_disable_multisig_link_from_email(UserforDisableMultisig.first_multisig_email, UserforDisableMultisig.email_password, "Freewallet", "Verify removing your confirmation email")
        securityPage.navigate_to_link(link1)
        loginPage.input_pincode_login(UserforDisableMultisig.pincode)
        securityPage.navigate_to_email_confirmation()
        securityPage.wait_and_assert_element_text(Multisig.email1, '')

    @pytest.mark.usefixtures("preset_for_delete_one_multisig_address")
    @xray("QA-1681")
    @pytest.mark.websmoke
    def test_delete_one_multisig_address(self, driver):
        loginPage = LoginPage(driver)
        loginPage.reset_session()
        loginPage.login_as_basic_user(UserforDeleteOneMultisigAddress.email, UserforMultisigTransaction.password)
        loginPage.input_pincode_login(UserforDeleteOneMultisigAddress.pincode)
        securityPage = SecurityPage(driver)
        securityPage.navigate_to_email_confirmation()
        securityPage.delete_one_multisig_address(UserforDeleteOneMultisigAddress.first_multisig_email)
        link = email.get_delete_one_multisig_address_link_from_email(UserforDeleteOneMultisigAddress.first_multisig_email, UserforDeleteOneMultisigAddress.email_password, "Freewallet", "Verify removing your confirmation email")
        securityPage.navigate_to_link(link)
        loginPage.input_pincode_login(UserforDeleteOneMultisigAddress.pincode)
        securityPage.navigate_to_email_confirmation()
        securityPage.wait_until_element_visible(Multisig.confirmedAddressFirst)
        securityPage.wait_and_assert_element_text(Multisig.confirmedAddressFirst, UserforDeleteOneMultisigAddress.second_multisig_email)

