import pytest
from Pages.LoginPage import *
from Pages.TransactionsPage import *
from Pages.DashboardPage import *
from Config.Users import *
from Helpers.SQLHelper import *
from Helpers.SMTPHelper import *
from Pages.Admin_Pages.AdminMainPage import *
from Pages.Admin_Pages.AdminLoginPage import *
from Pages.Admin_Pages.AdminTransactionsPage import *

@pytest.fixture(scope="function")
@pytest.mark.usefixtures("driver")
def login_as_basic_user(driver):
    loginPage = LoginPage(driver)
    loginPage.reset_session()
    loginPage.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
    loginPage.input_pincode_login(ExistingBasicUser.pincode)
    yield


class TestClass:

    def test_amountTooBig(driver):
        sql = SQLHelper()
        sql.set_settings_payouts_limits("user_amount_too_big_transfer", 0.000001)
        transactionsPage = TransactionsPage(driver)
        loginPage = LoginPage(driver)
        comment = str(time.time())
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_user_id("DOGE")
        transactionsPage.send_transaction_step_2_user_id(ExistingBasicUser.userID)
        transactionsPage.send_transaction_step_3("1")
        transactionsPage.send_transaction_step_4(comment)

