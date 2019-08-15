import pytest
from Pages.LoginPage import *
from Pages.TransactionsPage import *
from Config.Users import *
from Helpers.SQLHelper import *
from Locators.DashboardLocators import *

@pytest.fixture(scope='class')
def data_fixture():
    sql = SQLHelper()
    print("setup fixture")  # тут создаем дату
    yield print("data from fixture")  # тут магия (если нужны будут какие-то ресурсы)
    print("teardown")

@pytest.fixture(scope="function", autouse=True)
@pytest.mark.usefixtures("driver")
def loginAsBasicUser(driver):
    loginPage = LoginPage(driver)
    loginPage.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
    loginPage.input_pincode_login(ExistingBasicUser.pincode)


@pytest.mark.usefixtures("driver", "data_fixture")
class TestClass:

    # QA-842
    def test_sendTransactionToUserID(self, driver):
        comment = str(time.time())
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_to_user_id("BTC", "0.00000001", ExistingGoogleUser.userID, comment)
        transactionsPage.check_first_transaction("BTC", "0.00000001", comment)

