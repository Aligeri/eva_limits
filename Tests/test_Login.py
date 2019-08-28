import pytest
from Pages.LoginPage import *
from Config.Users import *
from Locators.DashboardLocators import DashboardLocators
from selenium.common.exceptions import WebDriverException

@pytest.fixture(scope='function', autouse=True)
@pytest.mark.usefixtures("driver")
def data_logout(driver):
    loginPage = LoginPage(driver)
    loginPage.reset_session()
    yield


@pytest.mark.usefixtures("driver", "data_logout")
class TestClass:


    def test_IncorrectPasswordLogin(self, driver):
        loginPage = LoginPage(driver)
        loginPage.login_as_basic_user("test@test.test", "12345678")
        loginPage.wait_and_assert_element_text(LoginPageLocators.incorrectPasswordTooltip, "Incorrect password")
        loginPage.get_base_url()

    def test_LoginAsBasicUser(self, driver):
        loginPage = LoginPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        loginPage.wait_until_element_visible(DashboardLocators.logout)
        loginPage.wait_and_assert_element_text(DashboardLocators.userName, ExistingBasicUser.userName)

    @pytest.mark.google
    def test_LoginAsGoogleUser(self, driver):
        loginPage = LoginPage(driver)
        loginPage.clear_google_cookies()
        loginPage.login_as_google_user(ExistingGoogleUser.email, ExistingGoogleUser.password)
        loginPage.input_pincode_login(ExistingGoogleUser.pincode)
        loginPage.wait_until_element_visible(DashboardLocators.logout)
        loginPage.wait_and_assert_element_text(DashboardLocators.userName, ExistingGoogleUser.userName)


    @pytest.mark.skip("Фейсбук блочит юзеров")
    def test_LoginAsFacebookUser(self, driver):
        loginPage = LoginPage(driver)
        loginPage.login_as_facebook_user(ExistingFacebookUser.email, ExistingFacebookUser.password)
        loginPage.input_pincode_login(ExistingFacebookUser.pincode)
        loginPage.wait_until_element_visible(DashboardLocators.logout)
        loginPage.wait_and_assert_element_text(DashboardLocators.userName, ExistingFacebookUser.userName)
