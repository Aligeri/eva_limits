from selenium.webdriver.common.by import By


class ReceiveWallets:
    btc = (By.XPATH, "//div[@data-currency='btc']//span")
    ardr = (By.XPATH, "//div[@data-currency='ardr']//span")
    bcc = (By.XPATH, "//div[@data-currency='bcc']//span")
    eth = (By.XPATH, "//div[@data-currency='eth']//span")
    eos = (By.XPATH, "//div[@data-currency='eos']//span")
    doge = (By.XPATH, "//div[@data-currency='doge']//span")
    xem = (By.XPATH, "//div[@data-currency='xem']//span")

class TopUpWallets:
    btc = (By.XPATH, "//h3[text()='Top up with other currencies']/following-sibling::div//div[@data-currency='btc']//span")
    ardr = (By.XPATH, "//h3[text()='Top up with other currencies']/following-sibling::div//div[@data-currency='ardr']//span")
    bcc = (By.XPATH, "//h3[text()='Top up with other currencies']/following-sibling::div//div[@data-currency='bcc']//span")
    eth = (By.XPATH, "//h3[text()='Top up with other currencies']/following-sibling::div//div[@data-currency='eth']//span")
    eos = (By.XPATH, "//h3[text()='Top up with other currencies']/following-sibling::div//div[@data-currency='eos']//span")
    doge = (By.XPATH, "//h3[text()='Top up with other currencies']/following-sibling::div//div[@data-currency='doge']//span")
    xem = (By.XPATH, "//h3[text()='Top up with other currencies']/following-sibling::div//div[@data-currency='xem']//span")

    depositAddress = (By.XPATH, "//div[@class='receive__wrapCurrentAddress--1qS_K']//div[contains(@class, 'receive__addressText--38aaT')]")

class DepositAddress:
    currentAddress = (By.XPATH, "//div[contains(@class, 'receive__addressText--38aaT')]")
    generateNew = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0 receive__generateNew--17KEh button__type-simple-small--2IN15')]")
    showAll = (By.XPATH, "//div[contains(@class, 'previews-address__showAll--1TynH')]")
    previousAddress1 = (By.XPATH, "//div[contains(@class, 'previews-address__wrapAddress--1lYXN')][1]")
    previousAddress2 = (By.XPATH, "//div[contains(@class, 'previews-address__wrapAddress--1lYXN')][2]")

    depositAddress = (By.XPATH, "//h3[text()='My deposit  address']/following-sibling::div[contains(@class, 'receive__addressText--38aaT')]")
    memo = (By.XPATH, "//h3[text()='Memo']/following-sibling::div[contains(@class, 'receive__addressText--38aaT')]")
    message = (By.XPATH, "//h3[text()='Message']/following-sibling::div[contains(@class, 'receive__addressText--38aaT')]")
    userId = (By.XPATH, "//div[contains(@class, 'receive__userId--3hHHB')]")
    link = (By.XPATH, "//a[@target='_blank']/b")
    minimumBlock = (By.XPATH, "//div[@class='receive__minimalBlock--y7xpq']")
    minimumAmount = (By.XPATH, "//div[@class='receive__minimalBlock--y7xpq']/b")