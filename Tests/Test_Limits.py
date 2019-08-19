import pytest
from Pages.LoginPage import *
from Pages.SecurityPage import *
from Config.Users import *
from Helpers.SQLHelper import *
from Locators.SecurityLocators import *


@pytest.fixture(scope='class')
def data_fixture(driver):
    sql = SQLHelper()
    sql.delete_limits_by_email_from_database(ExistingBasicUser.email)
    yield print("data from fixture")  # тут магия (если нужны будут какие-то ресурсы)
    sql.delete_limits_by_email_from_database(ExistingBasicUser.email)


@pytest.fixture(scope="function", autouse=True)
@pytest.mark.usefixtures("driver")
def login_as_basic_user(driver):
    loginPage = LoginPage(driver)
    loginPage.get_base_url()
    loginPage.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
    loginPage.input_pincode_login(ExistingBasicUser.pincode)


@pytest.mark.usefixtures("driver", "data_fixture")
class TestClass:

    @pytest.mark.skip("вынес тесты в другой файл")
    def test_ChangePincode(self, driver, url):
        securityPage = SecurityPage(driver)
        loginPage = LoginPage(driver)
        securityPage.navigate_to_pincode()
        securityPage.input_security_pincode_current(ExistingBasicUser.pincode)
        securityPage.input_security_pincode_new(ExistingBasicUser.changedPincode)
        securityPage.input_security_pincode_repeat(ExistingBasicUser.changedPincode)
        securityPage.wait_until_element_visible(SecurityPincode.successPopup)
        securityPage.refresh_page()
        loginPage.input_pincode_login(ExistingBasicUser.changedPincode)
        securityPage.input_security_pincode_current(ExistingBasicUser.changedPincode)
        securityPage.input_security_pincode_new(ExistingBasicUser.pincode)
        securityPage.input_security_pincode_repeat(ExistingBasicUser.pincode)
        securityPage.wait_until_element_visible(SecurityPincode.successPopup)

