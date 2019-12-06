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
