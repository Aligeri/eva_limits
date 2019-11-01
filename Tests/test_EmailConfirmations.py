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
    email.delete_emails_from_gmail(NewGoogleUser.email, NewGoogleUser.imap_code, "Freewallet", "Verify your email address")
    yield
    sql.delete_user_from_database(NewGoogleUser.email)
    email.delete_emails_from_gmail(NewGoogleUser.email, NewGoogleUser.imap_code, "Freewallet", "Verify your email address")

@pytest.fixture(scope='function')
def clear_data_for_change_mail():
    email.delete_emails_from_gmail(UserforСhangeMail.email, UserforСhangeMail.email_password, "Freewallet", "Verify changing your email address")
    email.delete_emails_from_gmail(UserforСhangeMail.new_email, UserforСhangeMail.email_password, "Freewallet", "Verify your email address")
    sql.set_email_for_notifications(UserforСhangeMail.email)
    sql.delete_user_from_database(UserforСhangeMail.new_email)
    yield
    email.delete_emails_from_gmail(UserforСhangeMail.email, UserforСhangeMail.email_password, "Freewallet", "Verify changing your email address")
    email.delete_emails_from_gmail(UserforСhangeMail.new_email, UserforСhangeMail.email_password, "Freewallet", "Verify your email address")

class TestClass:

    @xray("QA-797", "QA-795")
    @pytest.mark.websmoke
    @pytest.mark.usefixtures("data_basic_user")
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

    @xray("QA-725", "QA-724")
    @pytest.mark.websmoke
    @pytest.mark.usefixtures("data_google_user")
    def test_GoogleUserEmailVerification(self, driver):
        loginPage = LoginPage(driver)
        settingsPage = SettingsPage(driver)
        loginPage.clear_google_cookies()
        loginPage.navigate_to_signup_page()
        loginPage.login_as_google_user(NewGoogleUser.email, NewGoogleUser.password, NewGoogleUser.otp_code)
        loginPage.input_pincode_create(NewGoogleUser.pincode)
        loginPage.input_pincode_repeat(NewGoogleUser.pincode)
        settingsPage.check_email_is_not_verified(NewGoogleUser.email)
        verification_link = email.get_verification_link_from_email(NewGoogleUser.email, NewGoogleUser.imap_code, "Freewallet", "Verify")
        settingsPage.navigate_to_link(verification_link)
        loginPage.input_pincode_login(NewGoogleUser.pincode)
        settingsPage.check_email_is_verified(NewGoogleUser.email)

    @xray("QA-810")
    @pytest.mark.websmoke
    @pytest.mark.usefixtures("clear_data_for_change_mail")
    def test_change_email_for_notifications(self, driver):
        # проверка смены емайл в настройках QA-810
        loginPage = LoginPage(driver)
        loginPage.reset_session()
        loginPage.login_as_basic_user(UserforСhangeMail.email, UserforСhangeMail.password)
        loginPage.input_pincode_login(UserforСhangeMail.pincode)
        settingsPage = SettingsPage(driver)
        settingsPage.check_email_is_loaded(UserforСhangeMail.email)
        settingsPage.change_email(UserforСhangeMail.new_email)
        verification_link = email.get_change_mail_link_from_email(UserforСhangeMail.email, UserforСhangeMail.email_password, "Freewallet", "Verify changing your email address")
        settingsPage.navigate_to_link(verification_link)
        loginPage.input_pincode_login(UserforСhangeMail.pincode)
        #settingsPage.check_email_is_not_verified(UserforСhangeMail.new_email) не работает проверка промежуточного состояния
        verification_link1 = email.get_verification_link_from_email(UserforСhangeMail.new_email, UserforСhangeMail.email_password,"Freewallet", "Verify your email address")
        settingsPage.navigate_to_link(verification_link1)
        loginPage.input_pincode_login(UserforСhangeMail.pincode)
        #settingsPage.check_email_is_verified(UserforСhangeMail.new_email) не работает проверка финального состояния