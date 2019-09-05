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


@pytest.fixture(scope='function')
def email_unverified():
    yield
    sql = SQLHelper()
    sql.set_settings_payouts_limits("user_email_unverified", 1.00000001)

@pytest.fixture(scope='function')
def email_verified():
    yield
    sql = SQLHelper()
    sql.set_settings_payouts_limits("user_email_verified_only", 1.00000001)

@pytest.fixture(scope='function')
def amount_too_big():
    yield
    sql = SQLHelper()
    sql.set_settings_payouts_limits("user_amount_too_big", 1.00000001)

@pytest.fixture(scope='function')
def user_laundering():
    yield
    sql = SQLHelper()
    sql.set_settings_payouts_limits("user_laundering", 1)

@pytest.fixture(scope='function')
def amount_too_big_transfer():
    yield
    sql = SQLHelper()
    sql.set_settings_payouts_limits("user_amount_too_big_transfer", 1.00000001)

@pytest.fixture(scope='function')
def laundering_transfer():
    yield
    sql = SQLHelper()
    sql.set_settings_payouts_limits("user_laundering_transfer", 1.00000001)


@pytest.fixture(scope="function")
@pytest.mark.usefixtures("driver")
def login_as_basic_user(driver):
    loginPage = LoginPage(driver)
    loginPage.reset_session()
    loginPage.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
    loginPage.input_pincode_login(ExistingBasicUser.pincode)
    yield

@pytest.mark.usefixtures("driver")
class TestClass:

    @pytest.mark.usefixtures("login_as_basic_user", "amount_too_big")
    def test_amountTooBig(self, driver):
        sql = SQLHelper()
        sql.set_settings_payouts_limits("user_amount_too_big", 0.000001)
        transactionsPage = TransactionsPage(driver)
        dashboardPage = DashboardPage(driver)
        loginPage = LoginPage(driver)
        comment = str(time.time())
        dashboardPage.navigate_to_receive()
        dashboardPage.select_wallet("Dogecoin")
        dashboardPage.generate_new_deposit_address()
        currentAdresss = dashboardPage.get_current_deposit_address()
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_wallet_address("DOGE")
        transactionsPage.send_transaction_step_2_wallet_address(currentAdresss, "DOGE")
        transactionsPage.send_transaction_step_3(1)
        transactionsPage.send_transaction_step_4(comment)
        transaction_id = transactionsPage.get_transaction_ID_by_comment(comment)
        current_window = driver.current_window_handle
        admin_window = None
        driver.execute_script("window.open('https://board.cain.loc')")
        while admin_window is None:
            for handle in driver.window_handles:
                if handle != current_window:
                    admin_window = handle
        driver.switch_to.window(admin_window)
        adminLoginPage = AdminLoginPage(driver)
        adminMainPage = AdminMainPage(driver)
        adminTransactionsPage = AdminTransactionsPage(driver)
        adminLoginPage.login_as_admin_user("dwarf911@protonmail.com", "Kuzya910")
        adminMainPage.go_to_search_transaction()
        adminTransactionsPage.find_transaction_by_id(transaction_id)
        adminTransactionsPage.assert_manual_approve_transaction()


