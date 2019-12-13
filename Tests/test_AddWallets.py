import pytest
from Pages.LoginPage import *
from Pages.TransactionsPage import *
from Pages.BasePage import *
from Pages.AddWalletsPage import *
from Config.Users import *
from Config.Users import *
from Locators.AddWalletsLocators import *
from xrayplugin.plugin import xray

class TestClass:

    @xray("QA-1693")
    def test_add_wallets_currencies_availability(self, driver):
        loginPage = LoginPage(driver)
        loginPage.reset_session()
        loginPage.login_as_basic_user(UserforCheckAddWallets.email, UserforCheckAddWallets.password)
        loginPage.input_pincode_login(UserforCheckAddWallets.pincode)
        addWalletsPage = AddWalletsPage(driver)
        addWalletsPage.wait_and_click(AddWalletsElements.AddWalletsButton)
        addWalletsPage.wait_until_element_visible(Featured.FeaturedCardClickable)
        addWalletsPage.navigate_to_coins()
        addWalletsPage.wait_until_element_visible(Coins.CoinCircle)
        addWalletsPage.navigate_to_tokens()
        addWalletsPage.wait_until_element_visible(Tokens.TokenCircle)
