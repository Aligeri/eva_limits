import pytest
from Pages.LoginPage import *
from Pages.SettingsPage import *
from Pages.DashboardPage import *
from Config.Users import *
from Helpers.SQLHelper import *
from xrayplugin.plugin import xray


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
    yield
    sql.delete_user_from_database(NewBasicUser.email_848)

@pytest.fixture(scope="function")
def language_change(driver):
    loginPage = LoginPage(driver)
    sql.set_user_language(ExistingBasicUser.email1178, "en")
    loginPage.login_as_basic_user(ExistingBasicUser.email1178, ExistingBasicUser.password)
    loginPage.input_pincode_login(ExistingBasicUser.pincode)
    yield
    sql.set_user_language(ExistingBasicUser.email1178, "en")


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

    @pytest.mark.usefixtures("login_as_basic_user")
    @xray("QA-844", "QA-832")
    def test_buy_with_a_card(self, driver):
        dashboardPage = DashboardPage(driver)
        dashboardPage.navigate_to_buy_with_a_card()
        dashboardPage.select_buy_currency("ETH")
        dashboardPage.select_buy_currency("LTC")
        dashboardPage.select_buy_currency("BTC")

    @pytest.mark.usefixtures("login_as_basic_user")
    @pytest.mark.websmoke
    @xray("QA-834")
    def test_change_graphs(self, driver):
        dashboardPage = DashboardPage(driver)
        dashboardPage.wait_and_click(WalletActionsButtons.firstWallet)
        dashboardPage.select_graph_period("day")
        dashboardPage.select_graph_period("week")
        dashboardPage.select_graph_period("month")

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
        dashboard_page.check_receive_wallet("EOS", True)
