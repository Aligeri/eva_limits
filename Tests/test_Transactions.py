import pytest
from Pages.LoginPage import *
from Pages.TransactionsPage import *
from Config.Users import *
from Helpers.SQLHelper import *


@pytest.fixture(scope='function', autouse=True)
@pytest.mark.usefixtures("driver")
def data_logout(driver):
    loginPage = LoginPage(driver)
    loginPage.reset_session()
    yield print


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
    loginPage.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
    loginPage.input_pincode_login(ExistingBasicUser.pincode)
    yield


@pytest.fixture(scope="function")
@pytest.mark.usefixtures("driver")
def login_as_google_user(driver):
    loginPage = LoginPage(driver)
    loginPage.clear_google_cookies()
    loginPage.login_as_google_user(ExistingGoogleUser.email, ExistingGoogleUser.password)
    loginPage.input_pincode_login(ExistingGoogleUser.pincode)

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

    #@pytest.mark.google
    @pytest.mark.usefixtures("login_as_google_user")
    def test_sendTransactionWithNotVerifiedEmail(self, driver):
        comment = str(time.time())
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_to_user_id("BTC", "0.00000001", ExistingBasicUser.userID, comment)
        transactionsPage.check_not_verified_email_modal()
