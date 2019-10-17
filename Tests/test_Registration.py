import pytest
from Pages.LoginPage import *
from Config.Users import *
from Helpers.SQLHelper import *
from Locators.DashboardLocators import *
import time
import requests
from xrayplugin.plugin import xray

sql = SQLHelper()


@pytest.fixture(scope='function')
def data_basic_registration():
    yield
    sql.delete_user_from_database(NewBasicUser.email)


@pytest.fixture(scope='function')
def data_google_registration():
    yield
    sql.delete_user_from_database(NewGoogleUser.email)


@pytest.fixture(scope='class')
def data_facebook_registration():
    yield
    sql.delete_user_from_database(NewFacebookUser.email)



class TestClass:

    def test_PasswordsDoNotMatch(self, driver):
        loginPage = LoginPage(driver)
        loginPage.input_basic_user_registration_data('test1@test.test', '12345678', '12348765')
        loginPage.wait_and_click(LoginPageLocators.termsCheckbox)
        loginPage.assert_signup_button_state("disabled")
        loginPage.wait_and_assert_element_text(LoginPageLocators.incorrectPasswordTooltip, "Passwords don't match")


    def test_PasswordMustBe8Characters(self, driver):
        loginPage = LoginPage(driver)
        loginPage.input_basic_user_registration_data('test1@test.test', '1234')
        loginPage.assert_signup_button_state("disabled")
        loginPage.wait_and_assert_element_text(LoginPageLocators.incorrectPasswordTooltip, "Password must be at least 8 characters")


    @pytest.mark.usefixtures("data_basic_registration")
    @xray("QA-709", "QA-798")
    @pytest.mark.websmoke
    def test_BasicUserRegistration(self, driver):
        loginPage = LoginPage(driver)
        loginPage.input_basic_user_registration_data(NewBasicUser.email, NewBasicUser.password, NewBasicUser.password)
        loginPage.wait_and_click(LoginPageLocators.termsCheckbox)
        loginPage.assert_signup_button_state("enabled")
        loginPage.wait_and_click(LoginPageLocators.signUpButton)
        loginPage.input_pincode_create(NewBasicUser.pincode)
        loginPage.input_pincode_repeat(NewBasicUser.pincode)
        loginPage.wait_until_element_visible(DashboardLocators.logout)

    @pytest.mark.google
    @pytest.mark.usefixtures("data_google_registration")
    @xray("QA-727", "QA-693")
    @pytest.mark.websmoke
    def test_GoogleUserRegistration(self, driver):
        loginPage = LoginPage(driver)
        loginPage.navigate_to_signup_page()
        loginPage.clear_google_cookies()
        loginPage.login_as_google_user(NewGoogleUser.email, NewGoogleUser.password, NewGoogleUser.otp_code)
        loginPage.input_pincode_create(NewGoogleUser.pincode)
        loginPage.input_pincode_repeat(NewGoogleUser.pincode)
        loginPage.wait_until_element_visible(DashboardLocators.logout)

    @pytest.mark.skip("Фейсбук блочит юзеров")
    @pytest.mark.usefixtures("data_facebook_registration")
    @xray("QA-708", "QA-794")
    def test_FacebookUserRegistration(self, driver):
        loginPage = LoginPage(driver)
        loginPage.navigate_to_signup_page()
        loginPage.register_as_facebook_user(NewFacebookUser.email, NewFacebookUser.password)
        loginPage.input_pincode_create(NewFacebookUser.pincode)
        loginPage.input_pincode_repeat(NewFacebookUser.pincode)
        loginPage.wait_until_element_visible(DashboardLocators.logout)

    @xray("QA-802")
    def test_ExistingBasicUserRegistration(self, driver):
        loginPage = LoginPage(driver)
        loginPage.input_basic_user_registration_data(ExistingBasicUser.email, ExistingBasicUser.password, ExistingBasicUser.password)
        loginPage.wait_and_click(LoginPageLocators.termsCheckbox)
        loginPage.assert_signup_button_state("enabled")
        loginPage.wait_and_click(LoginPageLocators.signUpButton)
        loginPage.wait_and_assert_element_text(LoginPageLocators.incorrectPasswordTooltip, "Something went wrong. Try again later.")

    @xray("QA-799")
    def test_ExistingBasicUserRegistrationHigh(self, driver):
        loginPage = LoginPage(driver)
        loginPage.input_basic_user_registration_data(ExistingBasicUser.highEmail, ExistingBasicUser.password, ExistingBasicUser.password)
        loginPage.wait_and_click(LoginPageLocators.termsCheckbox)
        loginPage.assert_signup_button_state("enabled")
        loginPage.wait_and_click(LoginPageLocators.signUpButton)
        loginPage.wait_and_assert_element_text(LoginPageLocators.incorrectPasswordTooltip, "Something went wrong. Try again later.")

    @xray("QA-803")
    def test_ExistingGoogleUserRegistration(self, driver):
        loginPage = LoginPage(driver)
        loginPage.input_basic_user_registration_data(ExistingGoogleUser.email, ExistingGoogleUser.password, ExistingGoogleUser.password)
        loginPage.wait_and_click(LoginPageLocators.termsCheckbox)
        loginPage.assert_signup_button_state("enabled")
        loginPage.wait_and_click(LoginPageLocators.signUpButton)
        loginPage.wait_and_assert_element_text(LoginPageLocators.incorrectPasswordTooltip, "Something went wrong. Try again later.")

    @xray("QA-800")
    def test_ExistingGoogleUserRegistrationHigh(self, driver):
        loginPage = LoginPage(driver)
        loginPage.input_basic_user_registration_data(ExistingGoogleUser.highEmail, ExistingGoogleUser.password, ExistingGoogleUser.password)
        loginPage.wait_and_click(LoginPageLocators.termsCheckbox)
        loginPage.assert_signup_button_state("enabled")
        loginPage.wait_and_click(LoginPageLocators.signUpButton)
        loginPage.wait_and_assert_element_text(LoginPageLocators.incorrectPasswordTooltip, "Something went wrong. Try again later.")
