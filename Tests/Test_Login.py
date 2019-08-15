import pytest
from Pages.LoginPage import *
from Config.Users import *
from Locators.DashboardLocators import DashboardLocators


@pytest.fixture(scope='class')
def data_fixture():
    print("setup fixture")  # тут создаем дату
    yield print("data from fixture")  # тут магия (если нужны будут какие-то ресурсы)
    print("teardown fixture")  # тут удаляем дату


@pytest.mark.usefixtures("driver", "data_fixture")
class TestClass:

    def test_IncorrectPasswordLogin(self, driver):
        loginPage = LoginPage(driver)
        loginPage.login_as_basic_user("test@test.test", "12345678")
        loginPage.wait_and_assert_element_text(LoginPageLocators.incorrectPasswordTooltip, "Incorrect password")

    def test_LoginAsBasicUser(self, driver):
        loginPage = LoginPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        loginPage.wait_until_element_visible(DashboardLocators.logout)
        loginPage.wait_and_assert_element_text(DashboardLocators.userName, ExistingBasicUser.userName)

    def test_LoginAsGoogleUser(self, driver):
        loginPage = LoginPage(driver)
        loginPage.login_as_google_user(ExistingGoogleUser.email, ExistingGoogleUser.password)
        loginPage.input_pincode_login(ExistingGoogleUser.pincode)
        loginPage.wait_until_element_visible(DashboardLocators.logout)
        loginPage.wait_and_assert_element_text(DashboardLocators.userName, ExistingGoogleUser.userName)

    def test_LoginAsFacebookUser(self, driver):
        loginPage = LoginPage(driver)
        loginPage.login_as_facebook_user(ExistingFacebookUser.email, ExistingFacebookUser.password)
        loginPage.input_pincode_login(ExistingFacebookUser.pincode)
        loginPage.wait_until_element_visible(DashboardLocators.logout)
        loginPage.wait_and_assert_element_text(DashboardLocators.userName, ExistingFacebookUser.userName)
