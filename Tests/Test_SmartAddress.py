import pytest
from Pages.LoginPage import *
from Pages.DashboardPage import *
from Config.Users import *
from Helpers.SQLHelper import *
from Locators.DashboardLocators import *

@pytest.fixture(scope='class')
def data_fixture():
    sql = SQLHelper()
    print("setup fixture")  # тут создаем дату
    yield print("data from fixture")  # тут магия (если нужны будут какие-то ресурсы)
    print("teardown")

@pytest.fixture(scope="function", autouse=True)
@pytest.mark.usefixtures("driver")
def loginAsBasicUser(driver):
    loginPage = LoginPage(driver)
    loginPage.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
    loginPage.input_pincode_login(ExistingBasicUser.pincode)


@pytest.mark.usefixtures("driver", "data_fixture")
class TestClass:

    # QA-842
    def test_CheckBTCSmartAddressExist(self, driver):
        dashboardPage = DashboardPage(driver)
        dashboardPage.navigate_to_receive()
        dashboardPage.select_wallet("Bitcoin")
        dashboardPage.assert_deposit_address_is_not_empty()

    # QA-841, QA-840
    def test_GenerateBTCSmartAddress(self, driver):
        dashboardPage = DashboardPage(driver)
        dashboardPage.navigate_to_receive()
        dashboardPage.select_wallet("Bitcoin")
        currentAddress = dashboardPage.get_current_deposit_address()
        dashboardPage.generate_new_deposit_address(currentAddress)
        dashboardPage.checkPreviousAddressInList(currentAddress)
