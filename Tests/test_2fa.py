import pytest
from Pages.LoginPage import *
from Pages.SecurityPage import *
from Pages.TransactionsPage import *
from Pages.SettingsPage import *
from Config.Users import *
from Helpers.SQLHelper import *
from Locators.SecurityLocators import *
from xrayplugin.plugin import xray
from pyotp.totp import *


sql = SQLHelper()


@pytest.fixture(scope="function")
def data_665():
    sql.change_2fa_parameters_by_email(ExistingBasicUser.email695, "false", "false", "false")
    yield

@pytest.fixture(scope="function")
def data_698():
    sql.change_2fa_parameters_by_email(ExistingBasicUser.email698, "false", "true", "true")
    yield

@pytest.fixture(scope="function")
def data_699():
    sql.change_2fa_parameters_by_email(ExistingBasicUser.email699, "false", "false", "true")
    yield

@pytest.fixture(scope="function")
def data_702():
    sql.change_2fa_parameters_by_email(ExistingBasicUser.email702, "false", "true", "true")
    yield

@pytest.fixture(scope="function")
def data_666():
    sql.change_2fa_parameters_by_email(ExistingBasicUser.email666, "true", "true", "true")
    yield

@pytest.fixture(scope="function")
def data_664():
    sql.change_2fa_parameters_by_email(ExistingBasicUser.email664, "true", "true", "true")
    yield

class TestClass:

    @xray("QA-665", "QA-705")
    @pytest.mark.websmoke
    @pytest.mark.usefixtures("data_665")
    def test_add_2fa(self, driver):
        loginPage = LoginPage(driver)
        securityPage = SecurityPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email695, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        securityPage.navigate_to_2fa()
        activation_code = securityPage.get_2fa_activation_code()
        auth = TOTP(activation_code)
        securityPage.input_2fa(auth.now())
        securityPage.wait_and_click(TwoFactorAuth.closeButton)
        securityPage.wait_and_click(TwoFactorAuth.disable2fa)
        securityPage.input_2fa(auth.now())
        securityPage.wait_and_click(TwoFactorAuth.disableModal)

    @xray("QA-700")
    @pytest.mark.websmoke
    def test_2fa_transfer(self, driver):
        loginPage = LoginPage(driver)
        transactionsPage = TransactionsPage(driver)
        comment = str(time.time())
        auth = TOTP(ExistingBasicUser.email700_secret)
        loginPage.login_as_basic_user(ExistingBasicUser.email700, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_user_id("DOGE")
        transactionsPage.send_transaction_step_2_user_id(ExistingGoogleUser.userID)
        transactionsPage.send_transaction_step_3("1")
        transactionsPage.send_transaction_step_4(comment)
        code = auth.now()
        transactionsPage.input_2fa_and_send_transaction(code)
        transactionsPage.assert_transactions_page_displayed()

    @xray("QA-699")
    @pytest.mark.websmoke
    @pytest.mark.usefixtures("data_699")
    def test_add_2fa_to_transactions(self, driver):
        loginPage = LoginPage(driver)
        securityPage = SecurityPage(driver)
        transactionsPage = TransactionsPage(driver)
        comment = str(time.time())
        loginPage.login_as_basic_user(ExistingBasicUser.email699, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        securityPage.navigate_to_2fa()
        securityPage.check_2fa_checkbox_state("payout", "disabled")
        securityPage.enable_2fa_checkbox("payout")
        transactionsPage.navigate_to_dashboard()
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_user_id("DOGE")
        transactionsPage.send_transaction_step_2_user_id(ExistingGoogleUser.userID)
        transactionsPage.send_transaction_step_3("1")
        transactionsPage.send_transaction_step_4(comment)
        transactionsPage.wait_until_element_visible(TwoFactorAuth.code1)

    @xray("QA-698")
    @pytest.mark.websmoke
    @pytest.mark.usefixtures("data_698")
    def test_disable_2fa_from_transactions(self, driver):
        loginPage = LoginPage(driver)
        securityPage = SecurityPage(driver)
        transactionsPage = TransactionsPage(driver)
        comment = str(time.time())
        secret = sql.get_otp_secret_by_email(ExistingBasicUser.email698)
        auth = TOTP(secret[0])
        loginPage.login_as_basic_user(ExistingBasicUser.email698, ExistingBasicUser.password)
        loginPage.wait_until_element_visible(Pincode.title)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        securityPage.navigate_to_2fa()
        securityPage.check_2fa_checkbox_state("payout", "enabled")
        securityPage.disable_2fa_checkbox("payout", (auth.now()))
        transactionsPage.navigate_to_dashboard()
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_user_id("DOGE")
        transactionsPage.send_transaction_step_2_user_id(ExistingGoogleUser.userID)
        transactionsPage.send_transaction_step_3("1")
        transactionsPage.send_transaction_step_4(comment)
        transactionsPage.assert_transactions_page_displayed()

    @xray("QA-701")
    @pytest.mark.websmoke
    def test_incorrect_2fa(self, driver):
        loginPage = LoginPage(driver)
        securityPage = SecurityPage(driver)
        secret = sql.get_otp_secret_by_email(ExistingBasicUser.email701)
        auth = TOTP(secret[0])
        loginPage.login_as_basic_user(ExistingBasicUser.email701, ExistingBasicUser.password)
        code = "123456"
        if code != auth.now():
            authcode = code
        else:
            authcode = "654321"
        securityPage.input_2fa(authcode)
        loginPage.wait_and_assert_element_text(LoginPageLocators.incorrectPasswordTooltip, "5 attempts left")

    @xray("QA-702", "QA-659")
    @pytest.mark.websmoke
    @pytest.mark.usefixtures("data_702")
    def test_enable_login_2fa(self, driver):
        loginPage = LoginPage(driver)
        securityPage = SecurityPage(driver)
        secret = sql.get_otp_secret_by_email(ExistingBasicUser.email702)
        auth = TOTP(secret[0])
        loginPage.login_as_basic_user(ExistingBasicUser.email702, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        securityPage.navigate_to_2fa()
        securityPage.check_2fa_checkbox_state("login", "disabled")
        securityPage.enable_2fa_checkbox("login")
        loginPage.reset_session()
        loginPage.login_as_basic_user(ExistingBasicUser.email702, ExistingBasicUser.password)
        securityPage.input_2fa(auth.now())
        loginPage.wait_until_element_visible(Pincode.title)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)

    @xray("QA-666")
    @pytest.mark.usefixtures("data_666")
    def test_disable_login_2fa(self, driver):
        loginPage = LoginPage(driver)
        securityPage = SecurityPage(driver)
        secret = sql.get_otp_secret_by_email(ExistingBasicUser.email666)
        auth = TOTP(secret[0])
        loginPage.login_as_basic_user(ExistingBasicUser.email666, ExistingBasicUser.password)
        securityPage.input_2fa(auth.now())
        loginPage.wait_until_element_visible(Pincode.title)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        securityPage.navigate_to_2fa()
        securityPage.check_2fa_checkbox_state("login", "enabled")
        securityPage.disable_2fa_checkbox("login", (auth.now()))
        loginPage.reset_session()
        loginPage.login_as_basic_user(ExistingBasicUser.email666, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        loginPage.wait_and_assert_element_text(DashboardLocators.userName, "2fa disable user")


    @xray("QA-664")
    @pytest.mark.websmoke
    @pytest.mark.usefixtures("data_664")
    def test_disable_all_2fa_and_send_transaction(self, driver):
        loginPage = LoginPage(driver)
        securityPage = SecurityPage(driver)
        transactionsPage = TransactionsPage(driver)
        comment = str(time.time())
        secret = sql.get_otp_secret_by_email(ExistingBasicUser.email664)
        auth = TOTP(secret[0])
        loginPage.login_as_basic_user(ExistingBasicUser.email664, ExistingBasicUser.password)
        securityPage.input_2fa(auth.now())
        loginPage.wait_until_element_visible(Pincode.title)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        securityPage.navigate_to_2fa()
        securityPage.check_2fa_checkbox_state("login", "enabled")
        securityPage.check_2fa_checkbox_state("payout", "enabled")
        securityPage.check_2fa_checkbox_state("export", "enabled")
        securityPage.wait_and_click(TwoFactorAuth.disable2fa)
        securityPage.input_2fa(auth.now())
        securityPage.wait_and_click(TwoFactorAuth.disableModal)
        loginPage.reset_session()
        loginPage.login_as_basic_user(ExistingBasicUser.email664, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_user_id("DOGE")
        transactionsPage.send_transaction_step_2_user_id(ExistingGoogleUser.userID)
        transactionsPage.send_transaction_step_3("1")
        transactionsPage.send_transaction_step_4(comment)
        transactionsPage.assert_transactions_page_displayed()

    @xray("QA-933", "QA-934")
    def test_long_time_2fa_codes(self, driver):
        loginPage = LoginPage(driver)
        securityPage = SecurityPage(driver)
        transactionsPage = TransactionsPage(driver)
        comment = str(time.time())
        secret = sql.get_otp_secret_by_email(ExistingBasicUser.email933)
        auth = TOTP(secret[0])
        loginPage.login_as_basic_user(ExistingBasicUser.email933, ExistingBasicUser.password)
        long_code = auth.now()
        securityPage.input_2fa(long_code)
        loginPage.wait_until_element_visible(Pincode.title)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        time.sleep(30)
        loginPage.reset_session()
        loginPage.login_as_basic_user(ExistingBasicUser.email933, ExistingBasicUser.password)
        securityPage.input_2fa(long_code)
        loginPage.wait_until_element_visible(Pincode.title)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_user_id("DOGE")
        transactionsPage.send_transaction_step_2_user_id(ExistingGoogleUser.userID)
        transactionsPage.send_transaction_step_3("1")
        transactionsPage.send_transaction_step_4(comment)
        transactionsPage.input_2fa_and_send_transaction(long_code)
        transactionsPage.assert_transactions_page_displayed()

    @xray("QA-938")
    def test_long_time_2fa_export_mnemonic(self, driver):
        loginPage = LoginPage(driver)
        securityPage = SecurityPage(driver)
        settings_page = SettingsPage(driver)
        secret = sql.get_otp_secret_by_email(ExistingBasicUser.email933)
        auth = TOTP(secret[0])
        loginPage.login_as_basic_user(ExistingBasicUser.email933, ExistingBasicUser.password)
        long_code = auth.now()
        securityPage.input_2fa(long_code)
        loginPage.wait_until_element_visible(Pincode.title)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        #time.sleep(30)
        settings_page.check_email_is_loaded(ExistingBasicUser.email933)
        settings_page.navigate_to_export_wallet()
        settings_page.navigate_to_mnemonic()
        settings_page.wait_and_click(Mnemonic.gotIt)
        settings_page.wait_and_click(Mnemonic.generate)
        settings_page.generate_wallet_key()
        settings_page.wait_and_click(Mnemonic.continueButton)
        text = settings_page.get_element_text(Mnemonic.mnemonicKey)
        list = text.split(" ")
        settings_page.wait_and_click(Mnemonic.continueButton)
        settings_page.select_mnemonic_words(list)
        settings_page.wait_and_click(Mnemonic.continueButton)
        settings_page.wait_and_input_text(Mnemonic.thirdWordInput, list[2])
        settings_page.wait_to_be_clickable(Mnemonic.finishButton)
        settings_page.wait_and_click(Mnemonic.finishButton)
        securityPage.input_2fa(long_code)

    @xray("QA-932")
    def test_add_2fa_to_transactions(self, driver):
        loginPage = LoginPage(driver)
        securityPage = SecurityPage(driver)
        transactionsPage = TransactionsPage(driver)
        comment = str(time.time())
        secret = sql.get_otp_secret_by_email(ExistingBasicUser.email933)
        auth = TOTP(secret[0])
        loginPage.login_as_basic_user(ExistingBasicUser.email933, ExistingBasicUser.password)
        securityPage.input_2fa(auth.now())
        loginPage.wait_until_element_visible(Pincode.title)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        transactionsPage.navigate_to_dashboard()
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_user_id("DOGE")
        transactionsPage.send_transaction_step_2_user_id(ExistingGoogleUser.userID)
        transactionsPage.send_transaction_step_3("1")
        transactionsPage.send_transaction_step_4(comment)
        if auth.now() != "123456":
            transactionsPage.input_2fa_and_send_transaction("123456")
        else:
            transactionsPage.input_2fa_and_send_transaction("010101")
        transactionsPage.wait_until_element_visible(Send.twoFaTransactionError)
        transactionsPage.assert_element_text(Send.twoFaTransactionError, "Incorrect code")
