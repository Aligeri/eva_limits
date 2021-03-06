import pytest
from Pages.LoginPage import *
from Config.Users import *
from Locators.DashboardLocators import DashboardLocators
from selenium.common.exceptions import WebDriverException
from xrayplugin.plugin import xray



class TestClass:

    @xray("QA-720")
    def test_IncorrectPasswordLogin(self, driver):
        loginPage = LoginPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email, "12345678")
        loginPage.wait_and_assert_element_text(LoginPageLocators.incorrectPasswordTooltip, "The email and password you entered do not match our records. Please verify and try again")
        loginPage.get_base_url()

    @xray("QA-690", "QA-671")
    @pytest.mark.websmoke
    def test_LoginAsBasicUser(self, driver):
        loginPage = LoginPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        loginPage.wait_until_element_visible(DashboardLocators.logout)
        loginPage.wait_and_assert_element_text(DashboardLocators.userName, ExistingBasicUser.userName)

    @pytest.mark.google
    @xray("QA-683", "QA-658")
    @pytest.mark.websmoke
    def test_LoginAsGoogleUser(self, driver):
        loginPage = LoginPage(driver)
        loginPage.clear_google_cookies()
        loginPage.login_as_google_user(ExistingGoogleUser.email, ExistingGoogleUser.password, ExistingGoogleUser.otp_secret)
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
