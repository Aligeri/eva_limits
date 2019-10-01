import pytest
from Pages.LoginPage import *
from Pages.TransactionsPage import *
from Pages.DashboardPage import *
from Config.Users import *
from Helpers.SQLHelper import *
from Helpers.SMTPHelper import *
from Helpers.HostelHelper import *
from Pages.Admin_Pages.AdminMainPage import *
from Pages.Admin_Pages.AdminTransactionsPage import *


@pytest.fixture(scope='function')
def email_unverified():
    yield
    sql = SQLHelper()
    sql.set_settings_payouts_limits("user_email_unverified", 1.00000001)

@pytest.fixture(scope='function')
def user_email_verified_only():
    yield
    sql = SQLHelper()
    sql.set_settings_payouts_limits("user_email_verified_only", 1.00000001)

@pytest.fixture(scope='function')
def user_amount_too_big():
    yield
    sql = SQLHelper()
    sql.set_settings_payouts_limits("user_amount_too_big", 1.00000001)

@pytest.fixture(scope='function')
def user_laundering():
    yield
    sql = SQLHelper()
    sql.set_settings_payouts_limits("user_laundering", 1)

@pytest.fixture(scope='function')
def user_amount_too_big_transfer():
    yield
    sql = SQLHelper()
    sql.set_settings_payouts_limits("user_amount_too_big_transfer", 1.00000001)

@pytest.fixture(scope='function')
def user_laundering_transfer():
    yield
    sql = SQLHelper()
    sql.set_settings_payouts_limits("user_laundering_transfer", 1.00000001)

@pytest.fixture(scope='function')
def delete_user():
    yield
    sql = SQLHelper()
    sql.delete_user_from_database(NewBasicLimitBackend.email)


@pytest.fixture(scope="function")
@pytest.mark.usefixtures("driver")
def login_as_basic_user(driver):
    loginPage = LoginPage(driver)
    loginPage.reset_session()
    loginPage.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
    loginPage.input_pincode_login(ExistingBasicUser.pincode)
    yield

@pytest.fixture(scope="function")
def register_as_basic_user(driver):
    sql = SQLHelper()
    loginPage = LoginPage(driver)
    loginPage.input_basic_user_registration_data(NewBasicLimitBackend.email, NewBasicLimitBackend.password, NewBasicLimitBackend.password)
    loginPage.wait_and_click(LoginPageLocators.termsCheckbox)
    loginPage.assert_signup_button_state("enabled")
    loginPage.wait_and_click(LoginPageLocators.signUpButton)
    loginPage.input_pincode_create(NewBasicUser.pincode)
    loginPage.input_pincode_repeat(NewBasicUser.pincode)
    loginPage.wait_until_element_visible(DashboardLocators.logout)
    sql.verify_user_by_email(NewBasicLimitBackend.email)
    loginPage.refresh_page()
    loginPage.input_pincode_login(NewBasicUser.pincode)
    yield

@pytest.fixture(scope="function")
def verify_user_by_email(driver):
    yield
    sql = SQLHelper()
    sql.verify_user_by_email(ExistingBasicUser.email)



@pytest.mark.usefixtures("driver")
class TestClass:

    @pytest.mark.parametrize("limitName, values", [
        ("user_amount_too_big", 0.000001),
    ])
    @pytest.mark.usefixtures("login_as_basic_user", "user_amount_too_big")
    def test_amountTooBig(self, driver, limitName, values):
        """
        Тест на превышение лимита отправки суммы на новый адрес
        :param driver:
        :return:
        """
        sql = SQLHelper()
        hostel = HostelHelper()

        sql.set_settings_payouts_limits(limitName, values)
        transactionsPage = TransactionsPage(driver)
        dashboardPage = DashboardPage(driver)
        date = dashboardPage.get_current_time()
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
        hostel.check_status_transaction_by_email(ExistingBasicUser.email, date)




    @pytest.mark.parametrize("limitName, values", [
        ("user_email_verified_only", 0.000001),
    ])
    @pytest.mark.usefixtures("login_as_basic_user", "user_email_verified_only")
    def test_emailVerifiedOnlyConfirm(self, driver, limitName, values):
        sql = SQLHelper()
        sql.set_settings_payouts_limits(limitName, values)
        transactionsPage = TransactionsPage(driver)
        dashboardPage = DashboardPage(driver)
        comment = str(time.time())
        dashboardPage.navigate_to_receive()
        dashboardPage.select_wallet("Dogecoin")
        currentAdresss = dashboardPage.get_current_deposit_address()
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_wallet_address("DOGE")
        transactionsPage.send_transaction_step_2_wallet_address(currentAdresss, "DOGE")
        transactionsPage.send_transaction_step_3(1)
        transactionsPage.send_transaction_step_4(comment)
        transactionsPage.confirm_transaction_by_email()

    @pytest.mark.usefixtures("login_as_basic_user", "user_email_verified_only")
    def test_emailVerifiedOnlyCancel(self, driver):
        sql = SQLHelper()
        sql.set_settings_payouts_limits("user_email_verified_only", 0.000001)
        transactionsPage = TransactionsPage(driver)
        dashboardPage = DashboardPage(driver)
        comment = str(time.time())
        dashboardPage.navigate_to_receive()
        dashboardPage.select_wallet("Dogecoin")
        currentAdresss = dashboardPage.get_current_deposit_address()
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_wallet_address("DOGE")
        transactionsPage.send_transaction_step_2_wallet_address(currentAdresss, "DOGE")
        transactionsPage.send_transaction_step_3(1)
        transactionsPage.send_transaction_step_4(comment)
        transactionsPage.cancel_transaction_by_email()

    @pytest.mark.usefixtures("login_as_basic_user", "user_amount_too_big_transfer")
    def test_ammountTooBigTransfer(self, driver):
        sql = SQLHelper()
        hostel = HostelHelper()
        comment = str(time.time())
        sql.set_settings_payouts_limits("user_amount_too_big_transfer", 0.000001)
        transactionsPage = TransactionsPage(driver)
        dashboardPage = DashboardPage(driver)
        date = dashboardPage.get_current_time()
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_user_id("DOGE")
        transactionsPage.send_transaction_step_2_user_id("dwarf91111@gmail.com")
        transactionsPage.send_transaction_step_3(1)
        transactionsPage.send_transaction_step_4(comment)
        hostel.check_status_transaction_by_email(ExistingBasicUser.email, date)

    @pytest.mark.usefixtures("register_as_basic_user", "user_laundering", "delete_user")
    def test_userLaundering(self, driver):
        sql = SQLHelper()
        hostel = HostelHelper()
        comment = str(time.time())
        sql.set_settings_payouts_limits("user_laundering", 0.00000001)
        hostel.send_transaction("doge", sql.get_user_account_id(NewBasicLimitBackend.email)[0], "1000")
        transactionsPage = TransactionsPage(driver)
        dashboardPage = DashboardPage(driver)
        date = dashboardPage.get_current_time()
        comment = str(time.time())
        dashboardPage.navigate_to_receive()
        dashboardPage.select_wallet("Dogecoin")
        dashboardPage.generate_new_deposit_address()
        currentAdresss = dashboardPage.get_current_deposit_address()
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_wallet_address("DOGE")
        transactionsPage.send_transaction_step_2_wallet_address(currentAdresss, "DOGE")
        transactionsPage.send_transaction_step_3(999)
        transactionsPage.send_transaction_step_4(comment)
        hostel.check_status_transaction_by_email(NewBasicLimitBackend.email, date)

    @pytest.mark.usefixtures("register_as_basic_user", "user_laundering_transfer", "delete_user")
    def test_userLaunderingTransfer(self, driver):
        sql = SQLHelper()
        hostel = HostelHelper()
        comment = str(time.time())
        sql.set_settings_payouts_limits("user_laundering_transfer", 0.00000001)
        hostel.send_transaction("doge", sql.get_user_account_id(NewBasicLimitBackend.email)[0], "1000")
        transactionsPage = TransactionsPage(driver)
        dashboardPage = DashboardPage(driver)
        date = dashboardPage.get_current_time()
        comment = str(time.time())
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_user_id("DOGE")
        transactionsPage.send_transaction_step_2_user_id("dwarf91111@gmail.com")
        transactionsPage.send_transaction_step_3(999)
        transactionsPage.send_transaction_step_4(comment)
        hostel.check_status_transaction_by_email(NewBasicLimitBackend.email, date)


    @pytest.mark.usefixtures("login_as_basic_user", "email_unverified", "verify_user_by_email")
    def test_emailUnverified(self, driver):
        sql = SQLHelper()
        hostel = HostelHelper()
        comment = str(time.time())
        sql.set_settings_payouts_limits("user_email_unverified", 0.00000001)
        transactionsPage = TransactionsPage(driver)
        dashboardPage = DashboardPage(driver)
        date = dashboardPage.get_current_time()
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_user_id("DOGE")
        transactionsPage.send_transaction_step_2_user_id("dwarf91111@gmail.com")
        transactionsPage.send_transaction_step_3(1)
        sql.verify_user_by_email(ExistingBasicUser.email, "false")
        transactionsPage.send_transaction_step_4(comment)
        transactionsPage.check_canceled_transaction(comment, "Failed by exceeding of daily limits (strengthen security please)")










