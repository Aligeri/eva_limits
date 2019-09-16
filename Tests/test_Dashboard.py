import pytest
from Pages.LoginPage import *
from Pages.SettingsPage import *
from Pages.DashboardPage import *
from Config.Users import *
from Helpers.SQLHelper import *
from xrayplugin.plugin import xray


@pytest.fixture(scope='class')
def data_fixture():
    yield

@pytest.fixture(scope="function")
def login_as_basic_user(driver):
    loginPage = LoginPage(driver)
    sql = SQLHelper()
    sql.set_local_currency(ExistingBasicUser.email, "usd")
    loginPage.reset_session()
    loginPage.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
    loginPage.input_pincode_login(ExistingBasicUser.pincode)
    yield

@pytest.fixture(scope="function")
def language_change(driver):
    loginPage = LoginPage(driver)
    sql = SQLHelper()
    sql.set_user_language(ExistingBasicUser.email, "en")
    loginPage.reset_session()
    loginPage.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
    loginPage.input_pincode_login(ExistingBasicUser.pincode)
    yield
    sql.set_user_language(ExistingBasicUser.email, "en")

@pytest.mark.usefixtures("data_fixture")
class TestClass:

    @pytest.mark.usefixtures("login_as_basic_user")
    @pytest.mark.smoke
    @xray("QA-1047")
    def test_CheckFiatCurrency(self, driver):
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
    @pytest.mark.smoke
    @xray("QA-991")
    def test_ApplyFilters(self, driver):
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
    @pytest.mark.smoke
    @xray("QA-844", "QA-832")
    def test_buyWithACard(self, driver):
        dashboardPage = DashboardPage(driver)
        dashboardPage.navigate_to_buy_with_a_card()
        dashboardPage.select_buy_currency("ETH")
        dashboardPage.select_buy_currency("LTC")
        dashboardPage.select_buy_currency("BTC")

    @pytest.mark.usefixtures("login_as_basic_user")
    @pytest.mark.smoke
    @xray("QA-834")
    def test_ChangeGraphs(self, driver):
        dashboardPage = DashboardPage(driver)
        dashboardPage.wait_and_click(WalletActionsButtons.firstWallet)
        dashboardPage.select_graph_period("day")
        dashboardPage.select_graph_period("week")
        dashboardPage.select_graph_period("month")

    @pytest.mark.usefixtures("language_change")
    @pytest.mark.smoke
    @xray("QA-1178")
    def test_ChangeLanguage(self, driver):
        dashboardPage = DashboardPage(driver)
        dashboardPage.select_language("ja")
        dashboardPage.wait_and_assert_element_text(NavigationButtons.dashboard, "ダッシュボード")
        dashboardPage.wait_and_assert_element_text(NavigationButtons.settings, "設定")
        dashboardPage.wait_and_assert_element_text(NavigationButtons.security, "セキュリティ")

