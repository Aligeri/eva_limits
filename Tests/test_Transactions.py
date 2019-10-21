import pytest
from Pages.LoginPage import *
from Pages.TransactionsPage import *
from Pages.DashboardPage import *
from Config.Users import *
from Helpers.SQLHelper import *
from Helpers.SMTPHelper import *
from xrayplugin.plugin import xray


sql = SQLHelper()
email = SMTPHelper()


@pytest.fixture(scope="function")
def login_as_basic_user(driver):
    loginPage = LoginPage(driver)
    loginPage.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
    loginPage.input_pincode_login(ExistingBasicUser.pincode)
    yield


@pytest.fixture(scope="function")
def new_email_transaction(driver):
    loginPage = LoginPage(driver)
    sql.delete_user_from_database(UnregisteredBasicUser.email)
    email.delete_emails_from_gmail(MultisigGoogleUser.email, MultisigGoogleUser.imap_code, "Freewallet", "You've received 0.000001 XRP")
    loginPage.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
    loginPage.input_pincode_login(ExistingBasicUser.pincode)
    yield


@pytest.fixture(scope="function")
def login_as_google_user(driver):
    loginPage = LoginPage(driver)
    loginPage.clear_google_cookies()
    loginPage.login_as_google_user(ExistingGoogleUser.email, ExistingGoogleUser.password, ExistingGoogleUser.otp_secret)
    loginPage.input_pincode_login(ExistingGoogleUser.pincode)
    yield


class TestClass:

    @pytest.mark.usefixtures("login_as_basic_user")
    @xray("QA-746", "QA-740")
    @pytest.mark.websmoke
    def test_send_transaction_to_user_ID(self, driver):
        comment = str(time.time())
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_user_id("DOGE")
        transactionsPage.send_transaction_step_2_user_id(ExistingGoogleUser.userID)
        transactionsPage.send_transaction_step_3("1")
        transactionsPage.send_transaction_step_4(comment)
        transactionsPage.find_transaction_by_comment("DOGE", "1", comment)

    @pytest.mark.usefixtures("login_as_basic_user")
    @xray("QA-1084")
    def test_check_fiat_currency_value(self, driver):
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_user_id("DOGE")
        transactionsPage.send_transaction_step_2_user_id(ExistingGoogleUser.userID)
        transactionsPage.send_fiat_transaction_step_3("1.23")
        transactionsPage.check_fiat_transaction_step_4("1.23")

    @pytest.mark.usefixtures("login_as_basic_user")
    @xray("QA-745")
    @pytest.mark.websmoke
    def test_send_complex_transaction_to_user_ID(self, driver):
        comment = str(time.time())
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_complex_transaction_step_1("XRP")
        transactionsPage.send_complex_transaction_step_2("XRP", ExistingGoogleUser.xrtWallet, ExistingGoogleUser.xrtTag)
        transactionsPage.send_transaction_step_3("0.000001")
        transactionsPage.send_transaction_step_4(comment)
        transactionsPage.find_transaction_by_comment("XRP", "0.000001", comment)

    @pytest.mark.usefixtures("login_as_basic_user")
    @xray("QA-783")
    @pytest.mark.websmoke
    def test_send_failing_ETH_transaction_to_yourself(self, driver):
        comment = str(time.time())
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_wallet_address("ETH")
        transactionsPage.send_transaction_step_2_wallet_address(ExistingBasicUser.ethWallet, "ETH")
        transactionsPage.send_transaction_step_3("0.001")
        transactionsPage.send_transaction_step_4(comment)
        transactionsPage.find_transaction_by_comment("ETH", "0.00184", comment)
        transactionsPage.check_failed_transaction()

    @pytest.mark.usefixtures("login_as_basic_user")
    @xray("QA-749")
    @pytest.mark.websmoke
    def test_check_BTC_fees_displayed(self, driver):
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
    @xray("QA-756")
    @pytest.mark.websmoke
    def test_check_ETH_fees_not_displayed(self, driver):
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_wallet_address("ETH")
        transactionsPage.send_transaction_step_2_wallet_address(ExistingBasicUser.ethWallet, "ETH")
        transactionsPage.wait_and_input_text(Send.amount, "0.5")
        transactionsPage.wait_until_element_invisible(Send.normalFee)

    @pytest.mark.usefixtures("login_as_basic_user")
    @xray("QA-757")
    def test_check_include_exclude_fee(self, driver):
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_wallet_address("BTC")
        transactionsPage.send_transaction_step_2_wallet_address(ExistingBasicUser.btcWallet, "BTC")
        transactionsPage.wait_and_input_text(Send.amount, "0.001")
        transactionsPage.check_exclude_fee()
        transactionsPage.wait_and_click(Send.includeExcludeSwitch)
        transactionsPage.check_include_fee()

    @pytest.mark.usefixtures("login_as_basic_user")
    @xray("QA-1142")
    def test_check_send_all_fee(self, driver):
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_wallet_address("BTC")
        transactionsPage.send_transaction_step_2_wallet_address(ExistingBasicUser.btcWallet, "BTC")
        time.sleep(2)
        transactionsPage.wait_and_click(Send.sendAll)
        transactionsPage.check_include_fee()


    @pytest.mark.usefixtures("login_as_google_user")
    @xray("QA-721")
    def test_send_transaction_with_not_verified_email(self, driver):
        comment = str(time.time())
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_user_id("BTC")
        transactionsPage.send_transaction_step_2_user_id(ExistingBasicUser.userID)
        transactionsPage.send_transaction_step_3("0.00000001")
        transactionsPage.send_transaction_step_4(comment)
        transactionsPage.check_not_verified_email_modal()

    @pytest.mark.usefixtures("login_as_basic_user")
    @xray("QA-976")
    @pytest.mark.websmoke
    @pytest.mark.skip("Пуши в битрефиле не работают")
    def test_send_bitrefill_transaction(self, driver):
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_top_up_phone()
        transactionsPage.send_top_up_phone_transaction("+79050593996")
        transactionsPage.wait_and_click(TopUpPhone.historyButton)
        transactionsPage.check_first_transaction_comment("Top up phone")

    @pytest.mark.usefixtures("login_as_basic_user")
    @xray("QA-779")
    def test_check_ETH_token_transaction_failing(self, driver):
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_to_blocked_address("ETH", CommonData.unsupportedEthToken)

    @pytest.mark.usefixtures("login_as_basic_user")
    @xray("QA-778")
    @pytest.mark.websmoke
    def test_check_smart_contract_transaction_failing(self, driver):
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_to_blocked_address("ETH", CommonData.unsupportedSmartContract)

    @pytest.mark.usefixtures("login_as_basic_user")
    @xray("QA-777")
    @pytest.mark.websmoke
    def test_check_fwt_contract_transaction_failing(self, driver):
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_to_blocked_address("ETH", CommonData.FWTContract)


    @pytest.mark.usefixtures("login_as_basic_user")
    @xray("QA-782")
    @pytest.mark.websmoke
    def test_check_blocked_address_transaction_failing(self, driver):
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_to_blocked_address("DOGE", CommonData.blocked_gorgona_io)

    @pytest.mark.usefixtures("new_email_transaction")
    @xray("QA-743", "QA-763", "QA-796", "QA-742")
    @pytest.mark.websmoke
    def test_transaction_to_new_address(self, driver):
        comment = str(time.time())
        transactionsPage = TransactionsPage(driver)
        loginPage = LoginPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_user_id("XRP")
        transactionsPage.send_transaction_step_2_user_id(UnregisteredBasicUser.email)
        transactionsPage.send_transaction_step_3("0.000001")
        transactionsPage.send_transaction_step_4(comment)
        password_link = email.get_registration_link_from_email(MultisigGoogleUser.email, MultisigGoogleUser.imap_code, "Freewallet", "You've received 0.000001 XRP")
        password = transactionsPage.get_new_email_transfer_password(password_link)
        loginPage.reset_session()
        loginPage.login_as_basic_user(UnregisteredBasicUser.email, password)
        loginPage.input_pincode_create(UnregisteredBasicUser.pincode)
        loginPage.input_pincode_repeat(UnregisteredBasicUser.pincode)
        transactionsPage.check_first_transaction_receive("XRP", "0.000001", comment)


    @pytest.mark.usefixtures("login_as_basic_user")
    @xray("QA-744")
    @pytest.mark.websmoke
    def test_send_complex_transaction_to_user_email(self, driver):
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

    @pytest.mark.usefixtures("login_as_basic_user")
    @pytest.mark.skip("пуши не работают")
    @xray("QA-781")
    @pytest.mark.websmoke
    def test_cancel_transaction_without_hash(self, driver):
        transactionsPage = TransactionsPage(driver)
        comment = str(time.time())
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_user_id("BTC")
        transactionsPage.send_transaction_step_2_user_id(ExistingBasicUser.userID)
        transactionsPage.send_transaction_step_3("0.000006")
        transactionsPage.send_transaction_step_4(comment)
        transactionsPage.cancel_first_transaction_without_hash(comment)

    @pytest.mark.usefixtures("login_as_basic_user")
    @xray("QA-741")
    @pytest.mark.websmoke
    def test_check_minimum_amount(self, driver):
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_user_id("BTC")
        transactionsPage.send_transaction_step_2_user_id(ExistingGoogleUser.userID)
        transactionsPage.check_minimum_amount("0")

    @xray("QA-780")
    @pytest.mark.skip("Пуши для фейлов не работают")
    def test_send_double_spending_transaction(self, driver):
        comment = str(time.time())
        transactionsPage = TransactionsPage(driver)
        loginPage = LoginPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email_780, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        transactionsPage.navigate_to_send()
        transactionsPage.send_transaction_step_1_user_id("DOGE")
        transactionsPage.send_transaction_step_2_user_id(ExistingGoogleUser.userID)
        transactionsPage.send_transaction_step_3("1")
        transactionsPage.send_transaction_step_4(comment)
        transactionsPage.find_transaction_by_comment("DOGE", "1", comment)
        transactionsPage.navigate_to_send()
        comment_2 = str(time.time())
        transactionsPage.send_transaction_step_1_user_id("DOGE")
        transactionsPage.send_transaction_step_2_user_id(ExistingGoogleUser.userID)
        transactionsPage.send_transaction_step_3("1")
        transactionsPage.send_transaction_step_4(comment_2)
        transactionsPage.find_transaction_by_comment("DOGE", "1", comment_2)
        transactionsPage.check_doublespending_transaction(comment_2)