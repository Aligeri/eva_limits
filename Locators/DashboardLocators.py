from selenium.webdriver.common.by import By

class LanguageSelectors:
    en = (By.XPATH, "//button[@data-lang='en']")
    ru = (By.XPATH, "//button[@data-lang='ru']")
    ja = (By.XPATH, "//button[@data-lang='ja']")
    ko = (By.XPATH, "//button[@data-lang='ko']")
    fr = (By.XPATH, "//button[@data-lang='fr']")
    zhCN = (By.XPATH, "//button[@data-lang='zh-CN']")
    zhTW = (By.XPATH, "//button[@data-lang='zh-TW']")
    id = (By.XPATH, "//button[@data-lang='id']")
    obeliks = (By.XPATH, "//button[@data-lang='obeliks']")
    keys = (By.XPATH, "//button[@data-lang='keys']")

class NavigationButtons:
    dashboard = (By.XPATH, '//a[@href="/" and @class="header__link--1ckAu"]')
    settings = (By.XPATH, '//a[@href="/settings"]')
    security = (By.XPATH, '//a[@href="/security"]')
    logout = (By.XPATH, '//a[contains(@class, "header__logoutLink--uc90u header__link--1ckAu")]')

class WalletActionsButtons:
    history = (By.XPATH, "//div[@data-section='history']")
    send = (By.XPATH, "//div[@data-section='send']")
    receive = (By.XPATH, "//div[@data-section='receive']")
    topUpPhone = (By.XPATH, "//div[@data-section='top-up-phone']")
    buy = (By.XPATH, "//div[@data-section='buy']")

class DashboardLocators:
    logout = (By.XPATH, "//a[text()='Logout']")
    userName = (By.XPATH, "//div[contains(@class, 'header__userName--19bkR')]")
