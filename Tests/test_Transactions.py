import pytest
from Pages.LoginPage import *
from Pages.TransactionsPage import *
from Pages.DashboardPage import *
from Config.Users import *
from Helpers.SQLHelper import *

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
        transactionsPage.send_transaction_to_user_id("BTC", "0.00000001", ExistingGoogleUser.userID, comment)
        transactionsPage.check_first_transaction("BTC", "0.00000001", comment)

    @pytest.mark.usefixtures("login_as_basic_user")
    def test_sendComplexTransactionToUserID(self, driver):
        comment = str(time.time())
        transactionsPage = TransactionsPage(driver)
        loginPage = LoginPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_complex_transaction_to_user_id("XRP", "0.000001", ExistingGoogleUser.xrtWallet, ExistingGoogleUser.xrtTag, comment)
        transactionsPage.check_first_transaction("XRP", "0.000001", comment)

    @pytest.mark.usefixtures("login_as_basic_user")
    def test_sendFailingETHTransactionToYourself(self, driver):
        comment = str(time.time())
        transactionsPage = TransactionsPage(driver)
        loginPage = LoginPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_to_wallet_address("ETH", "0.001", ExistingBasicUser.ethWallet, "ETH", comment)
        transactionsPage.check_first_transaction("ETH", "0.00184", comment)
        transactionsPage.check_failed_transaction()

    @pytest.mark.usefixtures("login_as_basic_user")
    def test_checkBTCFeesDisplayed(self, driver):
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.show_fee_for_wallet_address("BTC", "0.00001", ExistingBasicUser.btcWallet, "BTC")
        transactionsPage.check_BTC_Fee("Low", "0.00008")
        transactionsPage.check_BTC_Fee("Normal", "0.00011")
        transactionsPage.check_BTC_Fee("Fast", "0.00013")
        transactionsPage.check_BTC_Fee("Urgent", "0.00016")

    @pytest.mark.usefixtures("login_as_basic_user")
    def test_checkIncludeExcludeFee(self, driver):
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.show_fee_for_wallet_address("BTC", "0.001", ExistingBasicUser.btcWallet, "BTC")
        transactionsPage.check_exclude_fee()
        transactionsPage.wait_and_click(Send.includeExcludeSwitch)
        transactionsPage.check_include_fee()


    @pytest.mark.usefixtures("login_as_google_user")
    def test_sendTransactionWithNotVerifiedEmail(self, driver):
        comment = str(time.time())
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_to_user_id("BTC", "0.00000001", ExistingBasicUser.userID, comment)
        transactionsPage.check_not_verified_email_modal()

    @pytest.mark.usefixtures("login_as_basic_user")
    def test_sendBitrefillTransaction(self, driver):
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_top_up_phone()
        transactionsPage.send_top_up_phone_transaction("+79050593996")
        transactionsPage.wait_and_click(TopUpPhone.historyButton)
        transactionsPage.check_first_transaction_comment("Top up phone")
