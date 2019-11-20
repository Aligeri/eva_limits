import pytest
from Pages.LoginPage import *
from Pages.SecurityPage import *
from Pages.TransactionsPage import *
from Pages.SettingsPage import *
from Config.Users import *
from Helpers.SQLHelper import *
from Locators.SecurityLocators import *
from xrayplugin.plugin import xray
from datetime import date
import os

sql = SQLHelper()

class TestClass:

    @xray("QA-1611")
    def test_russian_letters_in_KYS_fields(self, driver):
        loginPage = LoginPage(driver)
        settingsPage = SettingsPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email1611, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        settingsPage.navigate_to_identity()
        settingsPage.check_identity_errors("firstName", "Василий", "Name must be entered in Latin characters")
        settingsPage.check_identity_errors("secondName", "Петров", "Name must be entered in Latin characters")

    @xray("QA-1612")
    def test_symbols_in_KYS_fields(self, driver):
        loginPage = LoginPage(driver)
        settingsPage = SettingsPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email1611, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        settingsPage.navigate_to_identity()
        settingsPage.check_identity_errors("firstName", "Vasiliy-Petrov", "Name must be entered in Latin characters")
        settingsPage.check_identity_errors("secondName", "Petr, Vasilev", "Name must be entered in Latin characters")

    @xray("QA-1613")
    def test_today_date_in_KYS_fields(self, driver):
        loginPage = LoginPage(driver)
        settingsPage = SettingsPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email1611, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        settingsPage.navigate_to_identity()
        date_today = date.today().strftime("%d.%m.%Y")
        settingsPage.check_identity_errors("birthDate", date_today, "Incorrect data format")

    @xray("QA-1614")
    def test_18_years_ago_date_in_KYS_fields(self, driver):
        loginPage = LoginPage(driver)
        settingsPage = SettingsPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email1611, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        settingsPage.navigate_to_identity()
        date_today = date.today()
        date_18_years_ago = date_today.replace(year=date_today.year-18).strftime("%d.%m.%Y")
        settingsPage.assert_identity_error_not_displayed("birthDate", date_18_years_ago)


    @xray("QA-1615")
    def test_118_years_ago_date_in_KYS_fields(self, driver):
        loginPage = LoginPage(driver)
        settingsPage = SettingsPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email1611, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        settingsPage.navigate_to_identity()
        date_today = date.today()
        date_118_years_ago = date_today.replace(year=date_today.year-118).strftime("%d.%m.%Y")
        settingsPage.check_identity_errors("birthDate", date_118_years_ago, "Incorrect data format")

    @xray("QA-1616")
    def test_1_years_later_date_in_KYS_fields(self, driver):
        loginPage = LoginPage(driver)
        settingsPage = SettingsPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email1611, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        settingsPage.navigate_to_identity()
        date_today = date.today()
        date_1_year_later = date_today.replace(year=date_today.year + 1).strftime("%d.%m.%Y")
        settingsPage.check_identity_errors("birthDate", date_1_year_later, "Incorrect data format")

    @xray("QA-1617")
    def test_leap_year_date_in_KYS_fields(self, driver):
        loginPage = LoginPage(driver)
        settingsPage = SettingsPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email1611, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        settingsPage.navigate_to_identity()
        settingsPage.check_identity_errors("birthDate", "29.02.1999", "Incorrect data format")
        settingsPage.clear_input_text(Identity.birthDate)
        settingsPage.assert_identity_error_not_displayed("birthDate", "29.02.2000")

    @xray("QA-1618")
    def test_symbols_in_date_KYS_field(self, driver):
        loginPage = LoginPage(driver)
        settingsPage = SettingsPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email1611, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        settingsPage.navigate_to_identity()
        settingsPage.check_identity_errors("birthDate", "qwertyuiopasdfghjklzxcvbnm,./;\[]<>?:'\[p]!@#$%^&*()_+-=¡™£¢∞§¶•ªº", "Required")

    @xray("QA-1620")
    def test_low_size_file_in_KYS_fields(self, driver):
        loginPage = LoginPage(driver)
        settingsPage = SettingsPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email1611, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        settingsPage.navigate_to_identity()
        folder_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(folder_path, "data/low_size_file.png")
        settingsPage.check_identity_errors_file_upload("identityFile", file_path, "File size must be at least 500KB")
        settingsPage.check_identity_errors_file_upload("selfieFile", file_path, "File size must be at least 500KB")

    @xray("QA-1619")
    def test_high_size_file_in_KYS_fields(self, driver):
        loginPage = LoginPage(driver)
        settingsPage = SettingsPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email1611, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        settingsPage.navigate_to_identity()
        folder_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(folder_path, "data/high_size_file.png")
        settingsPage.check_identity_errors_file_upload("identityFile", file_path, "File size must be less than 10MB")
        settingsPage.check_identity_errors_file_upload("selfieFile", file_path, "File size must be less than 10MB")

    @xray("QA-1621")
    def test_normal_size_file_in_KYS_fields(self, driver):
        loginPage = LoginPage(driver)
        settingsPage = SettingsPage(driver)
        loginPage.login_as_basic_user(ExistingBasicUser.email1611, ExistingBasicUser.password)
        loginPage.input_pincode_login(ExistingBasicUser.pincode)
        settingsPage.navigate_to_identity()
        folder_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(folder_path, "data/normal_size_file.png")
        settingsPage.check_identity_error_not_displayed_file_upload("identityFile", file_path)
        settingsPage.check_identity_error_not_displayed_file_upload("selfieFile", file_path)