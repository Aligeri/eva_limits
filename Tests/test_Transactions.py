import pytest
from Pages.LoginPage import *
from Pages.TransactionsPage import *
from Pages.DashboardPage import *
from Config.Users import *
from Helpers.SQLHelper import *
from Helpers.SMTPHelper import *

"""
@pytest.fixture(scope='function', autouse=True)
@pytest.mark.usefixtures("driver")
def data_logout(driver):
    loginPage = LoginPage(driver)
    loginPage.reset_session()
    yield print
"""

@pytest.fixture(scope='class')
def data_fixture():
    sql = SQLHelper()
    print("setup fixture")  # тут создаем дату
    yield print("data from fixture")  # тут магия (если нужны будут какие-то ресурсы)
    print("teardown")


@pytest.fixture(scope="function")
@pytest.mark.usefixtures("driver")
def login_as_basic_user(driver):
    loginPage = LoginPage(driver)
    loginPage.reset_session()
    loginPage.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
    loginPage.input_pincode_login(ExistingBasicUser.pincode)
    yield

@pytest.fixture(scope="function")
@pytest.mark.usefixtures("driver")
def new_email_transaction(driver):
    sql = SQLHelper()
    smtp = SMTPHelper()
    loginPage = LoginPage(driver)
    sql.delete_user_from_database(UnregisteredBasicUser.email)
    smtp.delete_emails_from_gmail(MultisigGoogleUser.email, MultisigGoogleUser.password)
    loginPage.reset_session()
    loginPage.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
    loginPage.input_pincode_login(ExistingBasicUser.pincode)
    yield


@pytest.fixture(scope="function")
@pytest.mark.usefixtures("driver")
def login_as_google_user(driver):
    loginPage = LoginPage(driver)
    loginPage.clear_google_cookies()
    loginPage.reset_session()
    loginPage.login_as_google_user(ExistingGoogleUser.email, ExistingGoogleUser.password)
    loginPage.input_pincode_login(ExistingGoogleUser.pincode)
    yield

@pytest.mark.usefixtures("driver", "data_fixture")
class TestClass:

    # QA-842
    @pytest.mark.usefixtures("login_as_basic_user")
    def test_sendTransactionToUserID(self, driver):
        comment = str(time.time())
        transactionsPage = TransactionsPage(driver)
        loginPage = LoginPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_user_id("BTC")
        transactionsPage.send_transaction_step_2_user_id(ExistingGoogleUser.userID)
        transactionsPage.send_transaction_step_3("0.00000001")
        transactionsPage.send_transaction_step_4(comment)
        transactionsPage.check_first_transaction("BTC", "0.00000001", comment)

    @pytest.mark.usefixtures("login_as_basic_user")
    def test_sendComplexTransactionToUserID(self, driver):
        comment = str(time.time())
        transactionsPage = TransactionsPage(driver)
        loginPage = LoginPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_complex_transaction_step_1("XRP")
        transactionsPage.send_complex_transaction_step_2("XRP", ExistingGoogleUser.xrtWallet, ExistingGoogleUser.xrtTag)
        transactionsPage.send_transaction_step_3("0.000001")
        transactionsPage.send_transaction_step_4(comment)
        transactionsPage.check_first_transaction("XRP", "0.000001", comment)

    @pytest.mark.usefixtures("login_as_basic_user")
    def test_sendFailingETHTransactionToYourself(self, driver):
        comment = str(time.time())
        transactionsPage = TransactionsPage(driver)
        loginPage = LoginPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_wallet_address("ETH")
        transactionsPage.send_transaction_step_2_wallet_address(ExistingBasicUser.ethWallet, "ETH")
        transactionsPage.send_transaction_step_3("0.001")
        transactionsPage.send_transaction_step_4(comment)
        transactionsPage.check_first_transaction("ETH", "0.00184", comment)
        transactionsPage.check_failed_transaction()

    @pytest.mark.usefixtures("login_as_basic_user")
    def test_checkBTCFeesDisplayed(self, driver):
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_wallet_address("BTC")
        transactionsPage.send_transaction_step_2_wallet_address(ExistingBasicUser.btcWallet, "BTC")
        transactionsPage.wait_and_input_text(Send.amount, "0.00001")
        transactionsPage.check_BTC_Fee("Low", "0.00008")
        transactionsPage.check_BTC_Fee("Normal", "0.00011")
        transactionsPage.check_BTC_Fee("Fast", "0.00013")
        transactionsPage.check_BTC_Fee("Urgent", "0.00016")

    @pytest.mark.usefixtures("login_as_basic_user")
    def test_checkETHFeesNotDisplayed(self, driver):
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_wallet_address("ETH")
        transactionsPage.send_transaction_step_2_wallet_address(ExistingBasicUser.ethWallet, "ETH")
        transactionsPage.wait_and_input_text(Send.amount, "0.5")
        transactionsPage.wait_until_element_invisible(Send.normalFee)

    @pytest.mark.usefixtures("login_as_basic_user")
    def test_checkIncludeExcludeFee(self, driver):
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_wallet_address("BTC")
        transactionsPage.send_transaction_step_2_wallet_address(ExistingBasicUser.btcWallet, "BTC")
        transactionsPage.wait_and_input_text(Send.amount, "0.001")
        transactionsPage.check_exclude_fee()
        transactionsPage.wait_and_click(Send.includeExcludeSwitch)
        transactionsPage.check_include_fee()


    @pytest.mark.usefixtures("login_as_google_user")
    def test_sendTransactionWithNotVerifiedEmail(self, driver):
        comment = str(time.time())
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_user_id("BTC")
        transactionsPage.send_transaction_step_2_user_id(ExistingBasicUser.userID)
        transactionsPage.send_transaction_step_3("0.00000001")
        transactionsPage.send_transaction_step_4(comment)
        transactionsPage.check_not_verified_email_modal()

    @pytest.mark.usefixtures("login_as_basic_user")
    def test_sendBitrefillTransaction(self, driver):
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_top_up_phone()
        transactionsPage.send_top_up_phone_transaction("+79050593996")
        transactionsPage.wait_and_click(TopUpPhone.historyButton)
        transactionsPage.check_first_transaction_comment("Top up phone")

    @pytest.mark.usefixtures("login_as_basic_user")
    def test_checkETHTokenTransactionFailing(self, driver):
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_to_ETH_token("ETH", CommonData.unsupportedEthToken)

    @pytest.mark.usefixtures("new_email_transaction")
    def test_transactionToNewAddress(self, driver):
        comment = str(time.time())
        smtp = SMTPHelper()
        transactionsPage = TransactionsPage(driver)
        loginPage = LoginPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_user_id("XRP")
        transactionsPage.send_transaction_step_2_user_id(UnregisteredBasicUser.email)
        transactionsPage.send_transaction_step_3("0.000001")
        transactionsPage.send_transaction_step_4(comment)
        password_link = smtp.get_registration_link_from_email(MultisigGoogleUser.email, MultisigGoogleUser.password, "Freewallet", "You've received 0.000001 XRP")
        password = transactionsPage.get_new_email_transfer_password(password_link)
        loginPage.reset_session()
        loginPage.login_as_basic_user(UnregisteredBasicUser.email, password)
        loginPage.input_pincode_create(UnregisteredBasicUser.pincode)
        loginPage.input_pincode_repeat(UnregisteredBasicUser.pincode)
        transactionsPage.check_first_transaction_receive("XRP", "0.000001", comment)

    @pytest.mark.usefixtures("login_as_basic_user")
    def test_sendComplexTransactionToUserId(self, driver):
        transactionsPage = TransactionsPage(driver)
        loginPage = LoginPage(driver)
        comment = str(time.time())
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_user_id("XRP")
        transactionsPage.send_transaction_step_2_user_id(ExistingBasicVerifiedUser.userID)
        transactionsPage.send_transaction_step_3("0.00001")
        transactionsPage.send_transaction_step_4(comment)
        transactionsPage.wait_until_element_visible(Send.firstTransaction)
        loginPage.reset_session()
        loginPage.login_as_basic_user(ExistingBasicVerifiedUser.email, ExistingBasicVerifiedUser.password)
        loginPage.input_pincode_login(ExistingBasicVerifiedUser.pincode)
        transactionsPage.check_first_transaction_receive("XRP", "0.00001", comment)

    @pytest.mark.usefixtures("login_as_basic_user")
    def test_sendComplexTransactionToUserEmail(self, driver):
        transactionsPage = TransactionsPage(driver)
        loginPage = LoginPage(driver)
        comment = str(time.time())
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_user_id("XRP")
        transactionsPage.send_transaction_step_2_user_id(ExistingBasicVerifiedUser.email)
        transactionsPage.send_transaction_step_3("0.00001")
        transactionsPage.send_transaction_step_4(comment)
        transactionsPage.wait_until_element_visible(Send.firstTransaction)
        loginPage.reset_session()
        loginPage.login_as_basic_user(ExistingBasicVerifiedUser.email, ExistingBasicVerifiedUser.password)
        loginPage.input_pincode_login(ExistingBasicVerifiedUser.pincode)
        transactionsPage.check_first_transaction_receive("XRP", "0.00001", comment)