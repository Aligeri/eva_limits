import pytest
from Pages.LoginPage import *
from Pages.SettingsPage import *
from Pages.SecurityPage import *
from Config.Users import *
from Helpers.SQLHelper import *
from Helpers.SMTPHelper import *

@pytest.fixture(scope='function')
def data_basic_user():
    sql = SQLHelper()
    email = SMTPHelper()
    #email.delete_emails_from_gmail(NewBasicUser.email, NewBasicUser.password)
    yield print("data for basic user")  # тут магия (если нужны будут какие-то ресурсы)
    sql.delete_user_from_database(NewBasicUser.email)
    email.delete_emails_from_gmail(NewBasicUser.email, NewBasicUser.password)

@pytest.fixture(scope='function')
def data_google_user():
    sql = SQLHelper()
    email = SMTPHelper()
    #email.delete_emails_from_gmail(NewGoogleUser.email, NewGoogleUser.password)
    yield print("data for google user")  # тут магия (если нужны будут какие-то ресурсы)
    sql.delete_user_from_database(NewGoogleUser.email)
    email.delete_emails_from_gmail(NewGoogleUser.email, NewGoogleUser.password)

@pytest.mark.usefixtures("driver")
class TestClass:

    @pytest.mark.skip("Пока не разберусь с временем отправки емейлов")
    @pytest.mark.usefixtures("data_basic_user")
    def test_BasicUserEmailVerification(self, driver):
        loginPage = LoginPage(driver)
        settingsPage = SettingsPage(driver)
        email_agent = SMTPHelper()
        loginPage.input_basic_user_registration_data(NewBasicUser.email, NewBasicUser.password, NewBasicUser.password)
        loginPage.wait_and_click(LoginPageLocators.termsCheckbox)
        loginPage.assert_signup_button_state("enabled")
        loginPage.wait_and_click(LoginPageLocators.signUpButton)
        loginPage.input_pincode_create(NewBasicUser.pincode)
        loginPage.input_pincode_repeat(NewBasicUser.pincode)
        settingsPage.check_email_is_not_verified(NewBasicUser.email)
        verification_link = email_agent.get_verification_link_from_email(NewBasicUser.email, NewBasicUser.password, "Freewallet")
        settingsPage.navigate_to_link(verification_link)
        loginPage.input_pincode_login(NewBasicUser.pincode)
        settingsPage.check_email_is_verified(NewBasicUser.email)

    @pytest.mark.skip("Пока не разберусь с временем отправки емейлов")
    @pytest.mark.usefixtures("data_google_user")
    def test_GoogleUserEmailVerification(self, driver):
        loginPage = LoginPage(driver)
        settingsPage = SettingsPage(driver)
        email_agent = SMTPHelper()
        loginPage.navigate_to_signup_page()
        loginPage.login_as_google_user(NewGoogleUser.email, NewGoogleUser.password)
        loginPage.input_pincode_create(NewGoogleUser.pincode)
        loginPage.input_pincode_repeat(NewGoogleUser.pincode)
        settingsPage.check_email_is_not_verified(NewGoogleUser.email)
        verification_link = email_agent.get_verification_link_from_email(NewGoogleUser.email, NewGoogleUser.password, "Freewallet")
        settingsPage.navigate_to_link(verification_link)
        loginPage.input_pincode_login(NewGoogleUser.pincode)
        settingsPage.check_email_is_verified(NewGoogleUser.email)


