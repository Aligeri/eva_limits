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


class TestClass:

    @pytest.mark.usefixtures("login_as_basic_user")
    @xray("QA-974")
    @pytest.mark.websmoke
    def test_incorrect_phone_format(self, driver):
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_top_up_phone()
        transactionsPage.check_top_up_phone_validation("90000000", True, "Incorrect phone number format.")

    @pytest.mark.usefixtures("login_as_basic_user")
    @xray("QA-971")
    @pytest.mark.websmoke
    def test_incorrect_symbols_in_bitrefill(self, driver):
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_top_up_phone()
        transactionsPage.check_top_up_phone_validation("!@#$%^&*()_=-qwertyuiop[]asdfghjkl;'\zxcvbnm,./йцукенгшщзхъфывапролджэёячсмитьбю/", True)
        transactionsPage.assert_element_attirbute_value(TopUpPhone.mobileNumber, "value", "+")

    @pytest.mark.usefixtures("login_as_basic_user")
    @xray("QA-969")
    @pytest.mark.websmoke
    def test_operator_in_bitrefill(self, driver):
        transactionsPage = TransactionsPage(driver)
        transactionsPage.navigate_to_top_up_phone()
        transactionsPage.check_top_up_phone_validation(
            "+78005553535", False)
        transactionsPage.check_bitrefill_operator("Tele2")