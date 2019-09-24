import pytest
from Pages.LoginPage import *
from Pages.SettingsPage import *
from Pages.SecurityPage import *
from Config.Users import *
from Helpers.SQLHelper import *
from Helpers.SMTPHelper import *
from xrayplugin.plugin import xray

sql = SQLHelper()
email = SMTPHelper()

@pytest.fixture(scope='function')
def data_basic_user():
    email.delete_emails_from_gmail(NewBasicUser.email, NewBasicUser.password, "Freewallet", "Verify your email address")
    yield
    sql.delete_user_from_database(NewBasicUser.email)
    email.delete_emails_from_gmail(NewBasicUser.email, NewBasicUser.password, "Freewallet", "Verify your email address")

@pytest.fixture(scope='function')
def data_google_user():
    email.delete_emails_from_gmail(NewGoogleUser.email, NewGoogleUser.password, "Freewallet", "Verify your email address")
    yield
    sql.delete_user_from_database(NewGoogleUser.email)
    email.delete_emails_from_gmail(NewGoogleUser.email, NewGoogleUser.password, "Freewallet", "Verify your email address")

class TestClass:

    #@pytest.mark.skip("Пока не разберусь с временем отправки емейлов")
    @pytest.mark.usefixtures("data_basic_user")
    @xray("QA-797", "QA-795")
    @pytest.mark.smoke
    def test_BasicUserEmailVerification(self, driver):
        loginPage = LoginPage(driver)
        settingsPage = SettingsPage(driver)
        loginPage.input_basic_user_registration_data(NewBasicUser.email, NewBasicUser.password, NewBasicUser.password)
        loginPage.wait_and_click(LoginPageLocators.termsCheckbox)
        loginPage.assert_signup_button_state("enabled")
        loginPage.wait_and_click(LoginPageLocators.signUpButton)
        loginPage.input_pincode_create(NewBasicUser.pincode)
        loginPage.input_pincode_repeat(NewBasicUser.pincode)
        settingsPage.check_email_is_not_verified(NewBasicUser.email)
        verification_link = email.get_verification_link_from_email(NewBasicUser.email, NewBasicUser.password, "Freewallet", "Verify your email address")
        settingsPage.navigate_to_link(verification_link)
        loginPage.input_pincode_login(NewBasicUser.pincode)
        settingsPage.check_email_is_verified(NewBasicUser.email)

    #@pytest.mark.skip("Пока не разберусь с временем отправки емейлов")
    @pytest.mark.usefixtures("data_google_user")
    @xray("QA-725", "QA-724")
    @pytest.mark.smoke
    def test_GoogleUserEmailVerification(self, driver):
        loginPage = LoginPage(driver)
        settingsPage = SettingsPage(driver)
        loginPage.clear_google_cookies()
        loginPage.navigate_to_signup_page()
        loginPage.login_as_google_user(NewGoogleUser.email, NewGoogleUser.password)
        loginPage.input_pincode_create(NewGoogleUser.pincode)
        loginPage.input_pincode_repeat(NewGoogleUser.pincode)
        settingsPage.check_email_is_not_verified(NewGoogleUser.email)
        verification_link = email.get_verification_link_from_email(NewGoogleUser.email, NewGoogleUser.password, "Freewallet", "Verify")
        settingsPage.navigate_to_link(verification_link)
        loginPage.input_pincode_login(NewGoogleUser.pincode)
        settingsPage.check_email_is_verified(NewGoogleUser.email)


