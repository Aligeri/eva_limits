import pytest
from Pages.LoginPage import *
from Pages.SettingsPage import *
from Config.Users import *
from Helpers.SQLHelper import *
from Locators.DashboardLocators import *
from Helpers.SMTPHelper import *

@pytest.fixture(scope='class')
def data_fixture():
    sql = SQLHelper()
    email = SMTPHelper()
    #email.delete_emails_from_gmail(NewBasicUser.email, NewBasicUser.password)
    yield print("data from fixture")  # тут магия (если нужны будут какие-то ресурсы)
    sql.delete_user_from_database(NewBasicUser.email)
    email.delete_emails_from_gmail(NewBasicUser.email, NewBasicUser.password)

@pytest.mark.usefixtures("driver", "data_fixture")
class TestClass:


    def test_BasicUserEmailVerification(self, driver):
        loginPage = LoginPage(driver)
        settingsPage = SettingsPage(driver)
        email_agent = SMTPHelper()

        loginPage.input_basic_user_registration_data(NewBasicUser.email, NewBasicUser.password, NewBasicUser.password)
        waitAndClick(driver, LoginPageLocators.termsCheckbox)
        loginPage.assert_signup_button_state("enabled")
        loginPage.wait_and_click(LoginPageLocators.signUpButton)
        loginPage.input_pincode_create(NewBasicUser.pincode)
        loginPage.input_pincode_repeat(NewBasicUser.pincode)
        settingsPage.check_email_is_not_verified(NewBasicUser.email)
        verification_link = email_agent.get_verification_link_from_email(NewBasicUser.email, NewBasicUser.password, "Freewallet")
        settingsPage.navigate_to_link(verification_link)
        loginPage.input_pincode_login(NewBasicUser.pincode)
        settingsPage.check_email_is_verified(NewBasicUser.email)

