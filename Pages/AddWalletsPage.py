from Pages.BasePage import *
from Locators.AddWalletsLocators import *
import time

class AddWalletsPage(Page):

    def navigate_to_coins(self):
        self.wait_and_click(AddWalletsElements.CoinsTab)

    def navigate_to_tokens(self):
        self.wait_and_click(AddWalletsElements.TokensTab)