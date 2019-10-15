from selenium.webdriver.common.by import By


class NavigationLinks:
    userDetails = (By.XPATH, "//li[contains(@class, 'settings__tab--7oBOJ') and text()='User details']")
    account = (By.XPATH, "//li[contains(@class, 'settings__tab--7oBOJ') and text()='Account']")
    importWallet = (By.XPATH, "//li[contains(@class, 'settings__tab--7oBOJ') and text()='Import wallet']")
    exportWallet = (By.XPATH, "//li[contains(@class, 'settings__tab--7oBOJ') and text()='Export wallet']")

class Account:
    emailNotifications = (By.XPATH, "//input[contains(@class, 'settings__input--oMx6t styles__input--2cyn3')]")
    dangerText = (By.XPATH, "//div[contains(@class, 'settings__dangerDescription--24GPv settings__description--3sdDL')]")
    successText = (By.XPATH, "//div[contains(@class, 'settings__successDescription--IowBh settings__description--3sdDL')]")

class FiatCurrency:
    fiatCurrencyDropdown = (By.XPATH, "//select[@id='local-currency']")
    fiatUsd = (By.XPATH, "//option[@value='usd']")
    fiatEur = (By.XPATH, "//option[@value='eur']")
    fiatGbp = (By.XPATH, "//option[@value='gbp']")
    fiatRub = (By.XPATH, "//option[@value='rub']")

class userDetails:
    Name = (By.XPATH, "//input[@placeholder='Name']")
    UserId = (By.XPATH, "//input[@placeholder='User ID']")