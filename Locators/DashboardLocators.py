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
    firstWallet = (By.XPATH, "//a[contains(@class, 'wallets-widget__block--WcO-j')]")

class DashboardLocators:
    logout = (By.XPATH, "//a[text()='Logout']")
    userName = (By.XPATH, "//div[contains(@class, 'header__userName--19bkR')]")

class Fiat:
    totalFiat = (By.XPATH, "//div[contains(@class, 'total-balance-widget__subTitle--1FjUv')]")
    walletsFiat = (By.XPATH, "//div[contains(@class, 'wallets-widget__subTitle--3bxVy')]")
    graphFiat = (By.XPATH, "//span[contains(@class, 'graph-widget__statsPrice--19ETE')]")
    sendFiat = (By.XPATH, "//div[contains(@class, 'brick-wall__subTitle--2HsWj')]")

class Filters:
    filtersButton = (By.XPATH, "//button[contains(@class, 'filter-block__filterLink--1kp3W') and text()='Filters']")
    applyFilters = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0') and text()='Apply filters']")

    exchangeFilter = (By.XPATH, "//div[@class='filter-block__content--3zlIV']/a[contains(@class, 'tags__typeTag--22azq') and text()='Exchange']")
    payOutFilter = (By.XPATH, "//div[@class='filter-block__content--3zlIV']/a[contains(@class, 'tags__typeTag--22azq') and text()='Pay Out']")
    payInFilter = (By.XPATH, "//div[@class='filter-block__content--3zlIV']/a[contains(@class, 'tags__typeTag--22azq') and text()='Pay In']")
    failedFilter = (By.XPATH, "//div[@class='filter-block__content--3zlIV']/a[contains(@class, 'tags__typeTag--22azq') and text()='Failed']")

    exchangeButton = (By.XPATH, "//div[@class='filter-block__wrapper--3j5F2']/a[contains(@class, 'tags__typeTag--22azq') and text()='Exchange']")
    payOutButton = (By.XPATH, "//div[@class='filter-block__wrapper--3j5F2']/a[contains(@class, 'tags__typeTag--22azq') and text()='Pay Out']")
    payInButton = (By.XPATH, "//div[@class='filter-block__wrapper--3j5F2']/a[contains(@class, 'tags__typeTag--22azq') and text()='Pay In']")
    failedButton = (By.XPATH, "//div[@class='filter-block__wrapper--3j5F2']/a[contains(@class, 'tags__typeTag--22azq') and text()='Failed']")

    removeFilter = (By.XPATH, "//span[@class='svg-icon__svgIcon--216sc tags__removeIcon--SbaLA']")