from selenium.webdriver.common.by import By


class ReceiveWallets:
    btc = (By.XPATH, "//div[@data-currency='btc']//span")
    ardr = (By.XPATH, "//div[@data-currency='ardr']//span")
    bcc = (By.XPATH, "//div[@data-currency='bcc']//span")


class DepositAddress:
    currentAddress = (By.XPATH, "//div[contains(@class, 'receive__addressText--38aaT')]")
    generateNew = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0 receive__generateNew--17KEh button__type-simple-small--2IN15')]")
    showAll = (By.XPATH, "//div[contains(@class, 'previews-address__showAll--1TynH')]")
    previousAddress1 = (By.XPATH, "//div[contains(@class, 'previews-address__wrapAddress--1lYXN')][1]")
    previousAddress2 = (By.XPATH, "//div[contains(@class, 'previews-address__wrapAddress--1lYXN')][2]")