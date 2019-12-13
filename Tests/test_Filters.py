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
def login_as_filter_user(driver):
    loginPage = LoginPage(driver)
    loginPage.login_as_basic_user(ExistingBasicUser.email_filters, ExistingBasicUser.password)
    loginPage.input_pincode_login(ExistingBasicUser.pincode)
    yield


class TestClass:

    @pytest.mark.usefixtures("login_as_filter_user")
    @pytest.mark.websmoke
    @xray("QA-991")
    def test_transaction_type(self, driver):
        dashboardPage = DashboardPage(driver)
        exchange_transactions = ['–0.00095889 BTC\nComment "exchange btc to eth" (BTC to ETH)']
        pay_out_transactions = ['–0.00174 ETH\nComment "failing transaction"', '–0.00095889 BTC\nComment "exchange btc to eth" (BTC to ETH)', '–3 DOGE\nComment "simple doge to doge"']
        pay_in_transactions = ['+0.02963199 ETH\nFrom 0x59...06e8', '+2 DOGE\nFrom anonymous']
        transfer_in_transactions = ['+1 ETH\nFrom anonymous', '+1 BTC\nFrom anonymous', '+0.0001 XEM\nComment "xem transfer in"', '+0.001 ETH\nComment "eth transfer in"', '+10 DOGE\nComment "doge transfer in"', '+0.000001 BTC\nComment "btc transfer in"']
        transfer_out_transactions = []
        failed_transactions = ['–0.00174 ETH\nComment "failing transaction"']

        dashboardPage.apply_filter("Exchange")
        dashboardPage.compare_transactions(exchange_transactions)
        dashboardPage.remove_filter("Exchange")

        dashboardPage.apply_filter("Pay Out")
        dashboardPage.compare_transactions(pay_out_transactions)
        dashboardPage.remove_filter("Pay Out")

        dashboardPage.apply_filter("Pay In")
        dashboardPage.compare_transactions(pay_in_transactions)
        dashboardPage.remove_filter("Pay In")

        dashboardPage.apply_filter("Transfer In")
        dashboardPage.compare_transactions(transfer_in_transactions)
        dashboardPage.remove_filter("Transfer In")

        dashboardPage.apply_filter("Transfer Out")
        dashboardPage.compare_transactions(transfer_out_transactions)
        dashboardPage.remove_filter("Transfer Out")

        dashboardPage.apply_filter("Failed")
        dashboardPage.compare_transactions(failed_transactions)
        dashboardPage.remove_filter("Failed")

    @pytest.mark.usefixtures("login_as_filter_user")
    @pytest.mark.websmoke
    @xray("QA-994")
    def test_transaction_currency(self, driver):
        dashboardPage = DashboardPage(driver)
        ethereum_transactions = ['+0.02963199 ETH\nFrom 0x59...06e8', '–0.00174 ETH\nComment "failing transaction"', '+1 ETH\nFrom anonymous', '–0.00095889 BTC\nComment "exchange btc to eth" (BTC to ETH)', '+0.001 ETH\nComment "eth transfer in"']
        bitcoin_transactions = ['–0.00095889 BTC\nComment "exchange btc to eth" (BTC to ETH)', '+1 BTC\nFrom anonymous', '+0.000001 BTC\nComment "btc transfer in"']
        dogecoin_transactions = ['+2 DOGE\nFrom anonymous', '–3 DOGE\nComment "simple doge to doge"', '+10 DOGE\nComment "doge transfer in"']
        xem_transactions = ['+0.0001 XEM\nComment "xem transfer in"']

        dashboardPage.apply_filter("Ethereum")
        dashboardPage.compare_transactions(ethereum_transactions)
        dashboardPage.remove_filter("Ethereum")

        dashboardPage.apply_filter("Bitcoin")
        dashboardPage.compare_transactions(bitcoin_transactions)
        dashboardPage.remove_filter("Bitcoin")

        dashboardPage.apply_filter("Dogecoin")
        dashboardPage.compare_transactions(dogecoin_transactions)
        dashboardPage.remove_filter("Dogecoin")

        dashboardPage.apply_filter("XEM")
        dashboardPage.compare_transactions(xem_transactions)
        dashboardPage.remove_filter("XEM")


    @pytest.mark.websmoke
    @xray("QA-992")
    def test_date_filter(self, driver):

        dashboardPage = DashboardPage(driver)
        loginPage = LoginPage(driver)
        date_transactions = ['–1 DOGE\nComment "сщььуте"', '–0.00001 XEM\nComment "1572944050.16079"', '–0.00001 XEM\nComment "1572944045.268884"', '–0.000001 XEM\nComment "1572944014.052803"', '–0.00010193 BTC\nComment "1572944011.750589"', '–0.00001 XEM\nComment "1572944007.810615"', '–0.00184 ETH\nComment "1572943968.80063"', '–0.000001 XEM\nComment "1572943932.730963"', '–1 DOGE\nComment "1572943914.822861"', '–0.00000001 BTC\nComment "1572943786.968145"']

        loginPage.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)

        dashboardPage.apply_date_filters("11/05/2019", "11/05/2019")
        dashboardPage.compare_transactions(date_transactions)

    @pytest.mark.websmoke
    @xray("QA-993")
    def test_wrong_date_filter(self, driver):

        dashboardPage = DashboardPage(driver)
        loginPage = LoginPage(driver)

        loginPage.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)

        dashboardPage.apply_date_filters("not_a_date", "not_a_date")
        dashboardPage.wait_until_element_invisible(Filters.appliedFilter, 1)

    @pytest.mark.websmoke
    @xray("QA-997")
    def test_date_type_currency_filter(self, driver):

        dashboardPage = DashboardPage(driver)
        loginPage = LoginPage(driver)
        date_transactions = ['–0.00010193 BTC\nComment "1572944011.750589"']

        loginPage.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)

        dashboardPage.apply_date_filters("11/05/2019", "11/05/2019")
        dashboardPage.apply_filter("Failed")
        dashboardPage.apply_filter("Bitcoin")
        dashboardPage.compare_transactions(date_transactions)