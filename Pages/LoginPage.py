from Pages.BasePage import Page
from Helpers.CommonHelper import *
from Locators.LoginPageLocators import *
import time


class LoginPage(Page):

    # Метод для логина, принимает емейл + пароль
    def login_as_basic_user(self, username, password):
        self.wait_and_input_text(LoginPageLocators.loginField, username)
        self.wait_and_input_text(LoginPageLocators.passwordField, password)
        self.wait_to_be_clickable(LoginPageLocators.loginButton)
        self.wait_and_click(LoginPageLocators.loginButton)

    def login_as_google_user(self, google_email, google_password):
        main_page = self.driver.current_window_handle
        google_popup = None
        waitAndClick(self.driver, LoginPageLocators.google)
        while google_popup is None:
            for handle in self.driver.window_handles:
                if handle != main_page:
                    google_popup = handle
        self.driver.switch_to.window(google_popup)
        waitAndInputText(self.driver, LoginPageLocators.googleEmail, google_email)
        waitAndClick(self.driver, LoginPageLocators.googleEmailSubmit)
        waitAndInputText(self.driver, LoginPageLocators.googlePassword, google_password)
        waitAndClick(self.driver, LoginPageLocators.googlePasswordSubmit)
        self.driver.switch_to.window(main_page)

    def login_as_facebook_user(self, facebook_email, facebook_password):
        main_page = self.driver.current_window_handle
        facebook_popup = None
        waitAndClick(self.driver, LoginPageLocators.facebook)
        while facebook_popup is None:
            for handle in self.driver.window_handles:
                if handle != main_page:
                    facebook_popup = handle
        self.driver.switch_to.window(facebook_popup)
        waitAndInputText(self.driver, LoginPageLocators.facebookEmail, facebook_email)
        waitAndInputText(self.driver, LoginPageLocators.facebookPassword, facebook_password)
        waitAndClick(self.driver, LoginPageLocators.facebookLogin)
        self.driver.switch_to.window(main_page)

    def register_as_facebook_user(self, facebook_email, facebook_password):
        main_page = self.driver.current_window_handle
        facebook_popup = None
        waitAndClick(self.driver, LoginPageLocators.facebook)
        while facebook_popup is None:
            for handle in self.driver.window_handles:
                if handle != main_page:
                    facebook_popup = handle
        self.driver.switch_to.window(facebook_popup)
        waitAndInputText(self.driver, LoginPageLocators.facebookEmail, facebook_email)
        waitAndInputText(self.driver, LoginPageLocators.facebookPassword, facebook_password)
        waitAndClick(self.driver, LoginPageLocators.facebookLogin)
        waitAndClick(self.driver, LoginPageLocators.facebookConfirm)
        self.driver.switch_to.window(main_page)


    def login_as_mobile_user(self, mobile_phone):
        pass

    def navigate_to_signup_page(self):
        self.wait_and_click(LoginPageLocators.signUpLink)

    def input_basic_user_registration_data(self, email, password, repeat_password=''):
        waitAndClick(self.driver, LoginPageLocators.signUpLink)
        waitAndInputText(self.driver, LoginPageLocators.loginField, email)
        waitAndInputText(self.driver, LoginPageLocators.passwordField, password)
        waitAndInputText(self.driver, LoginPageLocators.repeatPasswordField, repeat_password)

    def assert_signup_button_state(self, state):
        if state == 'enabled':
            a = getElementAttribute(self.driver, LoginPageLocators.signUpButton, "disabled")
            assert getElementAttribute(self.driver, LoginPageLocators.signUpButton, "disabled") == None

        if state == 'disabled':
            a = getElementAttribute(self.driver, LoginPageLocators.signUpButton, "disabled")
            assert getElementAttribute(self.driver, LoginPageLocators.signUpButton, "disabled") == 'true'

    # Метод для ввода пин-кода при его создании, принимает пин-код в виде "1234"
    def input_pincode_create(self, pincode):
        pin_by_char = list(pincode)
        self.wait_and_input_text(Pincode.create1, pin_by_char[0])
        self.wait_and_input_text(Pincode.create2, pin_by_char[1])
        self.wait_and_input_text(Pincode.create3, pin_by_char[2])
        self.wait_and_input_text(Pincode.create4, pin_by_char[3])

    # Метод для повтора пин-кода при его создании, принимает пин-код в виде "1234"
    def input_pincode_repeat(self, pincode):
        pin_by_char = list(pincode)
        self.wait_and_input_text(Pincode.repeat1, pin_by_char[0])
        self.wait_and_input_text(Pincode.repeat2, pin_by_char[1])
        self.wait_and_input_text(Pincode.repeat3, pin_by_char[2])
        self.wait_and_input_text(Pincode.repeat4, pin_by_char[3])

    # Метод для повтора пин-кода при его логине, принимает пин-код в виде "1234"
    def input_pincode_login(self, pincode):
        pin_by_char = list(pincode)
        self.wait_and_input_text(Pincode.login1, pin_by_char[0])
        self.wait_and_input_text(Pincode.login2, pin_by_char[1])
        self.wait_and_input_text(Pincode.login3, pin_by_char[2])
        self.wait_and_input_text(Pincode.login4, pin_by_char[3])
