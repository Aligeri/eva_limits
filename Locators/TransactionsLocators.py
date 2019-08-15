from selenium.webdriver.common.by import By


class Send:
    btcWallet = (By.XPATH, "//a[contains(@class, 'brick-wall__item--1bMyi') and descendant::div[contains(text(), 'BTC')]]")
    ethWallet = (By.XPATH, "//a[contains(@class, 'brick-wall__item--1bMyi') and descendant::div[contains(text(), 'ETH')]]")
    userIdOrEmail = (By.XPATH, "//a[@class='brick-wall__item--1bMyi' and descendant::div[contains(text(), 'User ID or email')]]")
    continueButton1 = (By.XPATH, "//button[@class='button__button--2ccS0 send__buttonContinue--3pUpw']")
    continueButton2 = (By.XPATH, "//button[@class='button__button--2ccS0 send__buttonContinue--3pUpw']")
    continueButton3 = (By.XPATH, "//button[@class='button__button--2ccS0 send__buttonContinue--3pUpw']")
    sendToIdOrEmail = (By.XPATH, "//input[@placeholder='Enter user id or email']")
    amount = (By.XPATH, "//input[contains(@class, 'input__input--1lDmD') and @placeholder='0']")
    comment = (By.XPATH, "//input[contains(@class, 'input__input--1lDmD') and @placeholder='Enter comment (optional)']")
    withdraw = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0 send__buttonContinue--3pUpw')]")

    firstTransaction = (By.XPATH, "//a[@class='item__wrapper--2HY-h']")
    firstTransactionAmount = (By.XPATH, "//a[@class='item__wrapper--2HY-h'][1]//div[contains(@class, 'item__committed--24hSZ item__amount--3WcgV')]")
    firstTransactionComment = (By.XPATH, "//a[@class='item__wrapper--2HY-h'][1]//div[contains(@class, 'item__address--V6FmR')]")