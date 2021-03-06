import pytest
import time
from Pages.LoginPage import *
from Pages.SettingsPage import *
from Pages.DashboardPage import *
from Pages.TransactionsPage import *
from Config.Users import *
from Helpers.SQLHelper import *
from xrayplugin.plugin import xray
import random, string
from datetime import datetime


sql = SQLHelper()


@pytest.fixture(scope="function")
def login_as_basic_user(driver):
    loginPage = LoginPage(driver)
    sql.set_local_currency(ExistingBasicUser.email, "usd")
    loginPage.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
    loginPage.input_pincode_login(ExistingBasicUser.pincode)
    yield

@pytest.fixture(scope='class')
def data_new_user():
    sql.delete_user_from_database(NewBasicUser.email_848)
    yield
    sql.delete_user_from_database(NewBasicUser.email_848)

@pytest.fixture(scope='class')
def data_752():
    sql.delete_user_from_database(NewBasicUser.email_752)
    yield
    sql.delete_user_from_database(NewBasicUser.email_752)

@pytest.fixture(scope="function")
def language_change(driver):
    loginPage = LoginPage(driver)
    sql.set_user_language(ExistingBasicUser.email1178, "en")
    loginPage.login_as_basic_user(ExistingBasicUser.email1178, ExistingBasicUser.password)
    loginPage.input_pincode_login(ExistingBasicUser.pincode)
    yield
    sql.set_user_language(ExistingBasicUser.email1178, "en")

@pytest.fixture(scope="function")
def language_change_824(driver):
    sql.set_user_language(ExistingBasicUser.email_824, "en")
    yield
    sql.set_user_language(ExistingBasicUser.email_824, "en")


class TestClass:

    @pytest.mark.usefixtures("login_as_basic_user")
    @xray("QA-1047")
    def test_check_fiat_currency(self, driver):
        dashboardPage = DashboardPage(driver)
        settingsPage = SettingsPage(driver)
        loginPage = LoginPage(driver)
        dashboardPage.navigate_to_send()
        dashboardPage.checkFiatSymbols("$")
        dashboardPage.navigate_to_settings()
        settingsPage.change_fiat_currency("eur")
        dashboardPage.navigate_to_dashboard()
        dashboardPage.checkFiatSymbols("€")
        loginPage.refresh_page()
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        dashboardPage.checkFiatSymbols("€")
        dashboardPage.navigate_to_settings()
        settingsPage.change_fiat_currency("usd")

    @pytest.mark.usefixtures("login_as_basic_user")
    @pytest.mark.websmoke
    @xray("QA-991")
    def test_apply_filters(self, driver):
        dashboardPage = DashboardPage(driver)
        dashboardPage.apply_filter("Exchange")
        dashboardPage.apply_filter("Pay Out")
        dashboardPage.apply_filter("Pay In")
        dashboardPage.apply_filter("Failed")
        dashboardPage.remove_filter("Exchange")
        dashboardPage.remove_filter("Pay Out")
        dashboardPage.remove_filter("Pay In")
        dashboardPage.remove_filter("Failed")


    @pytest.mark.skip()
    @pytest.mark.websmoke
    @xray("QA-991")
    def test_apply_filters_po(self, driver):
        loginPage = LoginPage(driver)
        dashboardPage = DashboardPage(driver)
        transactionsPage = TransactionsPage(driver)

        loginPage.login_as_basic_user(ExistingBasicUser.email_808, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)

        dashboardPage.apply_filter("Exchange")
        comments = ['Comment "btc to eth comment" (BTC to ETH)']
        amounts = ['–0.00065 BTC']
        transactionsPage.check_transactions_on_page(comments, amounts)
        dashboardPage.remove_filter("Exchange")

        dashboardPage.apply_filter("Pay Out")
        comments = ['Comment "btc to eth comment" (BTC to ETH)']
        amounts = ['–0.00065 BTC']
        transactionsPage.check_transactions_on_page(comments, amounts)
        dashboardPage.remove_filter("Pay Out")

        dashboardPage.apply_filter("Pay In")
        comments = ['From 0x59...06e8']
        amounts = ['+0.02319903 ETH']
        transactionsPage.check_transactions_on_page(comments, amounts)
        dashboardPage.remove_filter("Pay Out")

    @pytest.mark.usefixtures("login_as_basic_user")
    @xray("QA-844", "QA-832")
    def test_buy_with_a_card(self, driver):
        dashboardPage = DashboardPage(driver)
        dashboardPage.navigate_to_buy_with_a_card()
        dashboardPage.select_buy_currency("ETH")
        dashboardPage.select_buy_currency("BTC")

    @pytest.mark.usefixtures("login_as_basic_user")
    @pytest.mark.websmoke
    @xray("QA-834", "QA-833")
    def test_change_graphs(self, driver):
        dashboardPage = DashboardPage(driver)
        dashboardPage.wait_and_click(WalletActionsButtons.firstWallet)
        dashboardPage.select_graph_period("day")
        dashboardPage.select_graph_period("week")
        dashboardPage.select_graph_period("month")

    @pytest.mark.usefixtures("language_change_824")
    @pytest.mark.websmoke
    @xray("QA-824")
    def test_change_language_in_settings(self, driver):
        dashboardPage = DashboardPage(driver)
        loginPage = LoginPage(driver)
        settingsPage = SettingsPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email_824, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        dashboardPage.navigate_to_settings()
        settingsPage.navigate_to_account()
        settingsPage.select_language_in_settings("ja")
        dashboardPage.wait_and_assert_element_text(NavigationButtons.dashboard, "ダッシュボード")
        dashboardPage.wait_and_assert_element_text(NavigationButtons.settings, "設定")
        dashboardPage.wait_and_assert_element_text(NavigationButtons.security, "セキュリティ")

    @pytest.mark.usefixtures("language_change")
    @pytest.mark.websmoke
    @xray("QA-1178")
    def test_change_language(self, driver):
        dashboardPage = DashboardPage(driver)
        dashboardPage.select_language("ja")
        dashboardPage.wait_and_assert_element_text(NavigationButtons.dashboard, "ダッシュボード")
        dashboardPage.wait_and_assert_element_text(NavigationButtons.settings, "設定")
        dashboardPage.wait_and_assert_element_text(NavigationButtons.security, "セキュリティ")

    @pytest.mark.usefixtures("data_new_user")
    @xray("QA-848")
    @pytest.mark.websmoke
    def test_new_user_receive(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        login_page.input_basic_user_registration_data(NewBasicUser.email_848, NewBasicUser.password, NewBasicUser.password)
        login_page.wait_and_click(LoginPageLocators.termsCheckbox)
        login_page.assert_signup_button_state("enabled")
        login_page.wait_and_click(LoginPageLocators.signUpButton)
        login_page.input_pincode_create(NewBasicUser.pincode)
        login_page.input_pincode_repeat(NewBasicUser.pincode)
        dashboard_page.navigate_to_receive()
        dashboard_page.check_receive_wallet("Bitcoin", False)
        dashboard_page.check_receive_wallet("Ethereum", False)
        dashboard_page.check_receive_wallet("XEM", True)

    @xray("QA-820")
    @pytest.mark.websmoke
    def test_ChangeName(self, driver):
        #проверка смены имени в настройках QA-820
        loginPage = LoginPage(driver)
        settingsPage = SettingsPage(driver)
        dashboardPage = DashboardPage(driver)
        loginPage.reset_session()
        loginPage.login_as_basic_user(UserforChangeName.email, UserforChangeName.password)
        loginPage.input_pincode_login(UserforChangeName.pincode)
        dashboardPage.navigate_to_settings()
        new_name = str(datetime.now().timestamp())

        settingsPage.change_name(new_name)
        settingsPage.navigate_to_dashboard()
        dashboardPage.wait_and_assert_element_text(DashboardLocators.userName, new_name)

    @pytest.mark.usefixtures("data_752")
    @xray("QA-752")
    @pytest.mark.websmoke
    def test_new_user_receive_minimum(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        login_page.input_basic_user_registration_data(NewBasicUser.email_752, NewBasicUser.password, NewBasicUser.password)
        login_page.wait_and_click(LoginPageLocators.termsCheckbox)
        login_page.assert_signup_button_state("enabled")
        login_page.wait_and_click(LoginPageLocators.signUpButton)
        login_page.input_pincode_create(NewBasicUser.pincode)
        login_page.input_pincode_repeat(NewBasicUser.pincode)
        dashboard_page.navigate_to_receive()
        dashboard_page.select_wallet("Bitcoin")
        dashboard_page.check_top_up_wallet("Ethereum", True)
        dashboard_page.check_top_up_wallet("Doge", True)
        dashboard_page.check_top_up_wallet("XEM", True)

    @xray("QA-983")
    @pytest.mark.skip("нет бккеша")
    @pytest.mark.websmoke
    def test_bitcoincash_ticker_in_receive(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        login_page.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
        login_page.input_pincode_login(ExistingBasicUser.pincode)
        dashboard_page.navigate_to_receive()
        dashboard_page.select_wallet("Bitcoin Cash")
        dashboard_page.check_value_in_deposit_address("bitcoincash:")

    @xray("QA-982")
    @pytest.mark.websmoke
    def test_doge_ticker_in_receive_not_displayed(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        login_page.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
        login_page.input_pincode_login(ExistingBasicUser.pincode)
        dashboard_page.navigate_to_receive()
        dashboard_page.select_wallet("Dogecoin")
        dashboard_page.check_value_not_in_deposit_address("doge")

    @xray("QA-822")
    @pytest.mark.websmoke
    def test_ChangeUserId(self, driver):
        #проверка смены user id в настройках QA-822
        loginPage = LoginPage(driver)
        loginPage.reset_session()
        loginPage.login_as_basic_user(UserforChangeUserId.email, UserforChangeUserId.password)
        loginPage.input_pincode_login(UserforChangeUserId.pincode)
        dashboardPage = DashboardPage(driver)
        dashboardPage.navigate_to_settings()
        settingsPage = SettingsPage(driver)
        new_user_id = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(8))
        settingsPage.change_user_id(new_user_id)
        settingsPage.navigate_to_dashboard()
        dashboardPage.navigate_to_receive()
        dashboardPage.check_receive_link('Dogecoin',new_user_id)
