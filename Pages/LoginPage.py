from Pages.BasePage import Page
from Locators.LoginPageLocators import *
from selenium.common.exceptions import WebDriverException
import time
from pyotp.totp import TOTP

class LoginPage(Page):

    def login_as_basic_user(self, username, password):
        """
        Метод для логина как basic-пользователь
        :param username: email пользователя
        :param password: пароль пользователя
        """
        self.wait_and_input_text(LoginPageLocators.loginField, username)
        self.wait_and_input_text(LoginPageLocators.passwordField, password)
        self.wait_to_be_clickable(LoginPageLocators.loginButton)
        self.wait_and_click(LoginPageLocators.loginButton)

    def login_as_google_user(self, google_email, google_password, otp_secret):
        """
        Метод для логина как G+ пользователь
        :param google_email: email пользователя на gmail
        :param google_password: пароль пользователя на gmail
        """
        main_page = self.driver.current_window_handle
        google_popup = None
        auth = TOTP(otp_secret)
        try:
            self.wait_and_click(LoginPageLocators.google)
            while google_popup is None:
                for handle in self.driver.window_handles:
                    if handle != main_page:
                        google_popup = handle
            self.driver.switch_to.window(google_popup)
            if self.get_element(LoginPageLocators.googleEmail, 1) == True:
                self.wait_and_input_text(LoginPageLocators.googleEmail, google_email)
                self.wait_and_click(LoginPageLocators.googleEmailSubmit)
                self.wait_and_input_text(LoginPageLocators.googlePassword, google_password)
                time.sleep(0.5)
                self.wait_and_click(LoginPageLocators.googlePasswordSubmit)
                self.wait_and_input_text(LoginPageLocators.totp, auth.now())
                self.wait_and_click(LoginPageLocators.totpSubmit)
            else:
                self.wait_and_click(LoginPageLocators.googleChangeAddress)
                self.wait_and_input_text(LoginPageLocators.googleEmail, google_email)
                self.wait_and_click(LoginPageLocators.googleEmailSubmit)
                self.wait_and_input_text(LoginPageLocators.googlePassword, google_password)
                time.sleep(0.5)
                self.wait_and_click(LoginPageLocators.googlePasswordSubmit)
                self.wait_and_input_text(LoginPageLocators.totp, auth.now())
                self.wait_and_click(LoginPageLocators.totpSubmit)
        except:
            self.driver.switch_to.window(main_page)
        self.driver.switch_to.window(main_page)

    def login_as_facebook_user(self, facebook_email, facebook_password):
        """
        Метод для логина как facebook-пользователь
        :param facebook_email: логин на facebook (email)
        :param facebook_password: пароль на facebook
        """
        main_page = self.driver.current_window_handle
        facebook_popup = None
        try:
            self.wait_and_click(LoginPageLocators.facebook)
            while facebook_popup is None:
                for handle in self.driver.window_handles:
                    if handle != main_page:
                        facebook_popup = handle
            self.driver.switch_to.window(facebook_popup)
            self.wait_and_input_text(LoginPageLocators.facebookEmail, facebook_email)
            self.wait_and_input_text(LoginPageLocators.facebookPassword, facebook_password)
            self.wait_and_click(LoginPageLocators.facebookLogin)
        except:
            self.driver.switch_to.window(main_page)
        self.driver.switch_to.window(main_page)

    def register_as_facebook_user(self, facebook_email, facebook_password):
        """
        Метод для регистрации как facebook-пользователь
        :param facebook_email: логин на facebook (email)
        :param facebook_password: пароль на facebook
        """
        main_page = self.driver.current_window_handle
        facebook_popup = None
        self.wait_and_click(LoginPageLocators.facebook)
        while facebook_popup is None:
            for handle in self.driver.window_handles:
                if handle != main_page:
                    facebook_popup = handle
        self.driver.switch_to.window(facebook_popup)
        self.wait_and_input_text(LoginPageLocators.facebookEmail, facebook_email)
        self.wait_and_input_text(LoginPageLocators.facebookPassword, facebook_password)
        self.wait_and_click(LoginPageLocators.facebookLogin)
        self.wait_and_click(LoginPageLocators.facebookConfirm)
        self.driver.switch_to.window(main_page)


    def login_as_mobile_user(self, mobile_phone):
        pass

    def navigate_to_signup_page(self):
        """
        Переход на страницу регистрации со страницы авторизации
        """
        self.wait_and_click(LoginPageLocators.signUpLink)

    def input_basic_user_registration_data(self, email, password, repeat_password=''):
        """
        Метод для ввода данных basic-пользователя на странице /auth/registration
        :param email: email basic-пользователя
        :param password: пароль basic-пользователя
        :param repeat_password: повторный пароль, по умолчанию пустое для проверки несоответствия паролей
        """
        self.wait_and_click(LoginPageLocators.signUpLink)
        self.wait_and_input_text(LoginPageLocators.loginField, email)
        self.wait_and_input_text(LoginPageLocators.passwordField, password)
        self.wait_and_input_text(LoginPageLocators.repeatPasswordField, repeat_password)

    def assert_signup_button_state(self, state):
        """
        Проверка состояния кнопки sign up на странице регистрации
        :param state: enabled для проверки что кнопка активна, disabled для проверки что кнопка неактивна
        """
        if state == 'enabled':
            self.wait_until_element_visible(LoginPageLocators.signUpButton)
            assert self.get_element_attribute(LoginPageLocators.signUpButton, "disabled") == None

        if state == 'disabled':
            self.wait_until_element_visible(LoginPageLocators.signUpButton)
            assert self.get_element_attribute(LoginPageLocators.signUpButton, "disabled") == 'true'

    def input_pincode_create(self, pincode):
        """
        Ввод пин-кода после регистрации в верхнее поле
        :param pincode: пин-код вида string из 4 цифр
        """
        pin_by_char = list(pincode)
        self.wait_and_input_text(Pincode.create1, pin_by_char[0])
        self.wait_and_input_text(Pincode.create2, pin_by_char[1])
        self.wait_and_input_text(Pincode.create3, pin_by_char[2])
        self.wait_and_input_text(Pincode.create4, pin_by_char[3])

    def input_pincode_repeat(self, pincode):
        """
        Ввод пин-кода после регистрации в нижнее поле (повтор)
        :param pincode: пин-код вида string из 4 цифр
        """
        pin_by_char = list(pincode)
        self.wait_and_input_text(Pincode.repeat1, pin_by_char[0])
        self.wait_and_input_text(Pincode.repeat2, pin_by_char[1])
        self.wait_and_input_text(Pincode.repeat3, pin_by_char[2])
        self.wait_and_input_text(Pincode.repeat4, pin_by_char[3])

    def input_pincode_login(self, pincode):
        """
        Ввод пин-кода после логина или обновления страницы
        :param pincode: пин-код вида string из 4 цифр
        """
        pin_by_char = list(pincode)
        self.wait_and_input_text(Pincode.login1, pin_by_char[0])
        self.wait_and_input_text(Pincode.login2, pin_by_char[1])
        self.wait_and_input_text(Pincode.login3, pin_by_char[2])
        self.wait_and_input_text(Pincode.login4, pin_by_char[3])

    def logout(self):
        """
        Метод для логаута со страниц, где видно кнопку Logout в хедере
        :return:
        """
        self.wait_and_click(LoginPageLocators.logoutLink)
        self.wait_and_click(LoginPageLocators.logoutButton)

    def clear_google_cookies(self):
        """
        Хитрый костыль для логаута гугл-юзеров, открывает вкладку с google.com, чистит cookies и возвращается на предыдующую вкладку
        :return:
        """
        current_window = self.driver.current_window_handle
        current_page = self.get_current_url()
        google_window = None
        self.driver.execute_script("window.open('https://www.google.com')")
        while google_window is None:
            for handle in self.driver.window_handles:
                if handle != current_window:
                    google_window = handle
        self.driver.switch_to.window(google_window)
        self.driver.delete_all_cookies()
        self.driver.close()
        self.driver.switch_to.window(current_window)
        self.driver.get(self.url)