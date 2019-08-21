from selenium.webdriver.common.by import By


class Send:
    btcWallet = (By.XPATH, "//a[contains(@class, 'brick-wall__item--1bMyi') and descendant::div[contains(text(), 'BTC')]]")
    ethWallet = (By.XPATH, "//a[contains(@class, 'brick-wall__item--1bMyi') and descendant::div[contains(text(), 'ETH')]]")
    xrpWallet = (By.XPATH, "//a[contains(@class, 'brick-wall__item--1bMyi') and descendant::div[contains(text(), 'XRP')]]")

    xrpRecieverWallet = (By.XPATH, "//a[contains(@class, 'brick-wall__item--1bMyi') and descendant::div[contains(text(), 'Ripple')]]")
    ethRecieverWallet = (By.XPATH, "//a[contains(@class, 'brick-wall__item--1bMyi') and descendant::div[text()='Ethereum']]")

    userIdOrEmail = (By.XPATH, "//a[contains(@class, 'brick-wall__item--1bMyi') and descendant::div[contains(text(), 'User ID or email')]]")
    userWalletAddress = (By.XPATH, "//a[contains(@class, 'brick-wall__item--1bMyi') and descendant::div[contains(text(), 'Wallet address')]]")

    continueButton1 = (By.XPATH, "//button[@class='button__button--2ccS0 send__buttonContinue--3pUpw']")
    continueButton2 = (By.XPATH, "//button[@class='button__button--2ccS0 send__buttonContinue--3pUpw']")
    continueButton3 = (By.XPATH, "//button[@class='button__button--2ccS0 send__buttonContinue--3pUpw']")
    sendToIdOrEmail = (By.XPATH, "//input[@placeholder='Enter user id or email']")
    sendToAddress = (By.XPATH, "//input[@placeholder='Enter address']")
    amount = (By.XPATH, "//input[contains(@class, 'input__input--1lDmD') and @placeholder='0']")
    comment = (By.XPATH, "//input[contains(@class, 'input__input--1lDmD') and @placeholder='Enter comment (optional)']")
    withdraw = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0 send__buttonContinue--3pUpw')]")
    destinationTag = (By.XPATH, "//input[contains(@class, 'input__input--1lDmD') and @placeholder='Enter destination tag']")

    firstTransaction = (By.XPATH, "//a[@class='item__wrapper--2HY-h']")
    firstTransactionAmount = (By.XPATH, "//a[contains(@class, 'item__wrapper--2HY-h')][1]//div[contains(@class, 'item__amount--3WcgV')]")
    firstTransactionComment = (By.XPATH, "//a[contains(@class, 'item__wrapper--2HY-h')][1]//div[contains(@class, 'item__address--V6FmR')]")

    firstErrorTransaction = (By.XPATH, "//a[contains(@class, 'item__wrapper--2HY-h item__wrapper__failed--16kTs')][1]")
    errorMessageInTransaction = (By.XPATH, "//td[text()='Error']/following-sibling::td")
    notVerifiedEmailModalMessage = (By.XPATH, "//div[contains(@class, 'pp__title--2cHYp pp__is-danger--3J_1v')]")