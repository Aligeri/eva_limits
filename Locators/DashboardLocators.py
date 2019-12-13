from selenium.webdriver.common.by import By

class LanguageSelectors:
    dropdown = (By.XPATH, "//div[contains(@class, 'language-selector__flag--1h7bx')]")
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
    dashboard = (By.XPATH, '//a[@href="/" and contains(@class, "header__link--1ckAu")]')
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
    transferInFilter = (By.XPATH, "//div[@class='filter-block__content--3zlIV']/a[contains(@class, 'tags__typeTag--22azq') and text()='Transfer In']")
    transferOutFilter = (By.XPATH, "//div[@class='filter-block__content--3zlIV']/a[contains(@class, 'tags__typeTag--22azq') and text()='Transfer Out']")

    ethereumFilter = (By.XPATH, "//div[@class='filter-block__content--3zlIV']//div[contains(@class, 'tags__iconCurrency--1naxG') and text()='Ethereum']")
    dogecoinFilter = (By.XPATH, "//div[@class='filter-block__content--3zlIV']//div[contains(@class, 'tags__iconCurrency--1naxG') and text()='Dogecoin']")
    bitcoinFilter = (By.XPATH, "//div[@class='filter-block__content--3zlIV']//div[contains(@class, 'tags__iconCurrency--1naxG') and text()='Bitcoin']")
    xemFilter = (By.XPATH, "//div[@class='filter-block__content--3zlIV']//div[contains(@class, 'tags__iconCurrency--1naxG') and text()='NEM']")

    exchangeButton = (By.XPATH, "//div[@class='filter-block__wrapper--3j5F2']/a[contains(@class, 'tags__typeTag--22azq') and text()='Exchange']")
    payOutButton = (By.XPATH, "//div[@class='filter-block__wrapper--3j5F2']/a[contains(@class, 'tags__typeTag--22azq') and text()='Pay Out']")
    payInButton = (By.XPATH, "//div[@class='filter-block__wrapper--3j5F2']/a[contains(@class, 'tags__typeTag--22azq') and text()='Pay In']")
    failedButton = (By.XPATH, "//div[@class='filter-block__wrapper--3j5F2']/a[contains(@class, 'tags__typeTag--22azq') and text()='Failed']")
    transferInButton = (By.XPATH, "//div[@class='filter-block__wrapper--3j5F2']/a[contains(@class, 'tags__typeTag--22azq') and text()='Transfer In']")
    transferOutButton = (By.XPATH, "//div[@class='filter-block__wrapper--3j5F2']/a[contains(@class, 'tags__typeTag--22azq') and text()='Transfer Out']")

    ethereumButton = (By.XPATH, "//div[@class='filter-block__wrapper--3j5F2']/a[contains(@class, 'tags__currencyTag--1mG4U') and //div[text()='Ethereum']]")
    dogecoinButton = (By.XPATH, "//div[@class='filter-block__wrapper--3j5F2']/a[contains(@class, 'tags__currencyTag--1mG4U') and //div[text()='Dogecoin']]")
    bitcoinButton = (By.XPATH, "//div[@class='filter-block__wrapper--3j5F2']/a[contains(@class, 'tags__currencyTag--1mG4U') and //div[text()='Bitcoin']]")
    xemButton = (By.XPATH, "//div[@class='filter-block__wrapper--3j5F2']/a[contains(@class, 'tags__currencyTag--1mG4U') and //div[text()='NEM']]")

    startDateFilter = (By.XPATH, "//input[@class='date-filter__input--264KP' and @placeholder='Start Date']")
    endDateFilter = (By.XPATH, "//input[@class='date-filter__input--264KP' and @placeholder='End Date']")

    removeFilter = (By.XPATH, "//span[@class='svg-icon__svgIcon--216sc tags__removeIcon--SbaLA']")

    appliedFilter = (By.XPATH, "//button[@class='tags__typeTag--22azq']")

    transaction = (By.XPATH, "//a[contains(@class, 'item__wrapper--2HY-h')]")

class BuyWithACard:
    bitcoin = (By.XPATH, "//div[contains(@class, 'wallets-select__currencyFrom--3N3t5') and @data-currency='btc']")
    ethereum = (By.XPATH, "//div[contains(@class, 'wallets-select__currencyFrom--3N3t5') and @data-currency='eth']")
    litecoin = (By.XPATH, "//div[contains(@class, 'wallets-select__currencyFrom--3N3t5') and @data-currency='ltc']")
    buyButton = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0 buy__submitButton--1miUq')]")

class Graph:
    day = (By.XPATH, ".//div[@data-period='day']")
    week = (By.XPATH, ".//div[@data-period='week']")
    month = (By.XPATH, ".//div[@data-period='month']")
    table = (By.XPATH, ".//div[contains(@class, 'graph-widget__tableData--1dvDO')]")
    chart = (By.XPATH, ".//div[contains(@class, 'graph-widget__chartWrapper--jbxzD')]")

class LimitLocks:
    dogeLock = (By.XPATH, "//span[contains(@class, 'currency-lib__icon-doge--3Xirh')]/following-sibling::span[contains(@class, 'icon-currency__lockedIcon--1xa_E')]")