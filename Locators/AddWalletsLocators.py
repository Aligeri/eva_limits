from selenium.webdriver.common.by import By

class AddWalletsElements:
    AddWalletsButton = (By.XPATH, "//a[contains(@class, 'wallets-widget__showEmptyWallets--2jsk7')]")
    FeaturedTab = (By.XPATH, "//li[contains(@class, 'wallets__tab--1N_nvJ') and text()='Featured']")
    CoinsTab = (By.XPATH, "//li[contains(@class, 'wallets__tab--1N_nv') and text()='Coins']")
    TokensTab = (By.XPATH, "//li[contains(@class, 'wallets__tab--1N_nv') and text()='Tokens']")
    SearchInput = (By.XPATH, "//input[contains(@class, 'wallets__input--3hgCH')]")


class Featured:
    FeaturedCard = (By.XPATH, "//div[contains(@class, 'feature-coin__coin--1n-cA')]")
    FeaturedCardClickable = (By.XPATH, "//div[contains(@class, 'feature-coin__coin--1n-cA feature-coin__clickable--15-vh')]")
    AddedIcon = (By.XPATH, "//span[contains(@class, 'svg-icon__svgIcon--216sc feature-coin__actionIcon--2_Np5 feature-coin__attached--NBy1y')]")
    AddIcon = (By.XPATH, "//span[contains(@class, 'svg-icon__svgIcon--216sc feature-coin__actionIcon--2_Np5')]")

class Coins:
    CoinCircle = (By.XPATH, "//div[contains(@class, 'icon-currency__currencyIcon--1QZfs icon-currency__circle--1_yET')]")
    AddedIcon = (By.XPATH, "//span[contains(@class, 'svg-icon__svgIcon--216sc coins__actionIcon--34Q5O coins__attached--1NJJt')]")
    AddIcon = (By.XPATH, "//span[contains(@class, 'svg-icon__svgIcon--216sc coins__actionIcon--34Q5O')]")

class Tokens:
    TokenCircle = (By.XPATH, "//div[contains(@class, 'icon-currency__currencyIcon--1QZfs icon-currency__circle--1_yET')]")
    AddedIcon = (By.XPATH, "//span[contains(@class, 'svg-icon__svgIcon--216sc coins__actionIcon--34Q5O coins__attached--1NJJt')]")
    AddIcon = (By.XPATH, "//span[contains(@class, 'svg-icon__svgIcon--216sc coins__actionIcon--34Q5O')]")
