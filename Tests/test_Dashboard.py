import pytest
from Pages.LoginPage import *
from Pages.SettingsPage import *
from Pages.DashboardPage import *
from Config.Users import *
from Helpers.SQLHelper import *


@pytest.fixture(scope='class')
def data_fixture():
    yield

@pytest.fixture(scope="function")
@pytest.mark.usefixtures("driver")
def login_as_basic_user(driver):
    loginPage = LoginPage(driver)
    sql = SQLHelper()
    sql.set_local_currency(ExistingBasicUser.email, "usd")
    loginPage.reset_session()
    loginPage.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
    loginPage.input_pincode_login(ExistingBasicUser.pincode)
    yield

@pytest.mark.usefixtures("driver", "data_fixture")
class TestClass:

    @pytest.mark.usefixtures("login_as_basic_user")
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
    def test_buyWithACard(self, driver):
        dashboardPage = DashboardPage(driver)
        dashboardPage.navigate_to_buy_with_a_card()
        dashboardPage.select_buy_currency("ETH")
        dashboardPage.select_buy_currency("LTC")
        dashboardPage.select_buy_currency("BTC")





