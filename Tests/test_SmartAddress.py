import pytest
from Pages.LoginPage import *
from Pages.DashboardPage import *
from Config.Users import *
from Helpers.SQLHelper import *
from xrayplugin.plugin import xray


@pytest.fixture(scope="function", autouse=True)
def loginAsBasicUser(driver):
    loginPage = LoginPage(driver)
    loginPage.login_as_basic_user(ExistingBasicVerifiedUser.email, ExistingBasicVerifiedUser.password)
    loginPage.input_pincode_login(ExistingBasicVerifiedUser.pincode)


class TestClass:

    # QA-842
    @xray("QA-842")
    @pytest.mark.websmoke
    def test_CheckBTCSmartAddressExist(self, driver):
        dashboardPage = DashboardPage(driver)
        dashboardPage.navigate_to_receive()
        dashboardPage.select_wallet("Bitcoin")
        dashboardPage.assert_deposit_address_is_not_empty()

    # QA-841, QA-840
    @xray("QA-841", "QA-840")
    @pytest.mark.websmoke
    def test_GenerateBTCSmartAddress(self, driver):
        dashboardPage = DashboardPage(driver)
        dashboardPage.navigate_to_receive()
        dashboardPage.select_wallet("Bitcoin")
        currentAddress = dashboardPage.get_current_deposit_address()
        dashboardPage.check_new_deposit_address(currentAddress)
        dashboardPage.check_previous_address_in_list(currentAddress)
