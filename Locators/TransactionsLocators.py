from selenium.webdriver.common.by import By


class Send:
    btcWallet = (By.XPATH, "//div[contains(@class, 'brick-wall__textWrapper--2PYAE')][div[contains(text(), 'BTC')]]")
    ethWallet = (By.XPATH, "//div[contains(@class, 'brick-wall__textWrapper--2PYAE')][div[contains(text(), 'ETH')]]")
    xrpWallet = (By.XPATH, "//div[contains(@class, 'brick-wall__textWrapper--2PYAE')][div[contains(text(), 'XRP')]]")
    dogeWallet = (By.XPATH, "//div[contains(@class, 'brick-wall__textWrapper--2PYAE')][div[contains(text(), 'DOGE')]]")
    xemWallet = (By.XPATH, "//div[contains(@class, 'brick-wall__textWrapper--2PYAE')][div[contains(text(), 'XEM')]]")

    xrpRecieverWallet = (By.XPATH, "//a[contains(@class, 'brick-wall__item--1bMyi') and descendant::div[contains(text(), 'Ripple')]]")
    ethRecieverWallet = (By.XPATH, "//a[contains(@class, 'brick-wall__item--1bMyi') and descendant::div[text()='Ethereum']]")
    btcRecieverWallet = (By.XPATH, "//a[contains(@class, 'brick-wall__item--1bMyi') and descendant::div[text()='Bitcoin']]")
    dogeRecieverWallet = (By.XPATH, "//a[contains(@class, 'brick-wall__item--1bMyi') and descendant::div[text()='Dogecoin']]")
    xemRecieverWallet = (By.XPATH, "//a[contains(@class, 'brick-wall__item--1bMyi') and descendant::div[contains(text(), 'NEM')]]")

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
    destinationTag = (By.XPATH, "//input[contains(@class, 'input__input--1lDmD') and @placeholder='Enter destination tag']|//input[contains(@class, 'input__input--1lDmD') and @placeholder='Enter message']")
    limitExceededTooltip = (By.CLASS_NAME, 'tippy-tooltip-content')
    tokenError = (By.XPATH, "//div[@class='send__tokenError--7Q4J_']")
    changeToFiat = (By.XPATH, "//span[contains(@class, 'svg-icon__svgIcon--216sc send__switchToFiatIcon--H1xig')]")
    fiatAmount = (By.XPATH, "//div[contains(@class, 'send__transactionAmountInFiat--1cKZg send__fiatAmount--2FKe5')]")
    sendAll = (By.XPATH, "//span[contains(@class, 'send__sendAllButton--3kNGM')]")

    networkFee = (By.XPATH, ".//div[@class='send__feeBlock--3EjJC']/div[1]")
    arrivalAmount = (By.XPATH, ".//h4[contains(text(), 'Arrival amount')]")
    totalWithFee = (By.XPATH, ".//h4[text()='Total amount']/span")
    includeExcludeSwitch = (By.XPATH, "//span[contains(@class, 'send__feeToggler--15oOJ')]")

    lowFee = (By.XPATH, "//div[contains(@class, 'send__tab--22xga') and text()='Low']")
    normalFee = (By.XPATH, "//div[contains(@class, 'send__tab--22xga') and text()='Normal']")
    fastFee = (By.XPATH, "//div[contains(@class, 'send__tab--22xga') and text()='Fast']")
    urgentFee = (By.XPATH, "//div[contains(@class, 'send__tab--22xga') and text()='Urgent']")

    firstTransaction = (By.XPATH, ".//a[@class='item__wrapper--2HY-h']")
    firstTransactionAmount = (By.XPATH, ".//a[contains(@class, 'item__wrapper--2HY-h')][1]//div[contains(@class, 'item__amount--3WcgV')]")
    firstTransactionComment = (By.XPATH, ".//a[contains(@class, 'item__wrapper--2HY-h')][1]//div[contains(@class, 'item__address--V6FmR')]")

    firstErrorTransaction = (By.XPATH, ".//a[contains(@class, 'item__wrapper--2HY-h item__wrapper__failed--16kTs')][1]")
    errorMessageInTransaction = (By.XPATH, ".//td[text()='Error']/following-sibling::td")
    notVerifiedEmailModalMessage = (By.XPATH, ".//div[contains(@class, 'pp__title--2cHYp pp__is-danger--3J_1v')]")

    firstUnconfirmedTransaction = (By.XPATH, ".//a[contains(@class, 'item__wrapper--2HY-h item__wrapper__unconfirmed--3YAln')][1]")
    statusInTransaction = (By.XPATH, "//tr[@class='transaction-view__statusRow--3b34v']/td[2]")
    cancelButtonInTransaction = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0') and text()='Cancel']")

    newEmailTransferPassword = (By.XPATH, "//h1/span[@style='color: #000;']")

    confirm2fa = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0 button__type-inline--3PR1T button__color-full-red--1bKJL')]")
    twoFaTransactionError = (By.XPATH, "//div[@class='pop-ups__error--2VlGh']")

    transactionBlock = (By.XPATH, '//a[contains(@class, "item__wrapper--2HY-h")]')
    commentBlock = (By.XPATH, "//div[contains(@class, 'item__address--V6FmR')]")
    amountBlock = (By.XPATH, "//div[contains(@class, 'item__amount--3WcgV')]")


class TopUpPhone:
    mobileNumber = (By.XPATH, "//input[contains(@class, 'mobile-pay-section__input--bGf8n')]")
    continueButton = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0')]")
    firstPaymentValue = (By.XPATH, "//div[contains(@class, 'mobile-pay-section__package--di8ED')][1]")
    sendCoinsButton = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0') and text()='Send coins']")
    successModal = (By.XPATH, "//div[contains(@class, 'mobile-pay-section__header--b5oUb')]")
    historyButton = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0') and text()='History']")
    errorMessage = (By.XPATH, "//div[contains(@class, 'mobile-pay-section__incorrectNumberErrorBlock--L_KSu')]")
    logo = (By.XPATH, "//img[contains(@class, 'mobile-pay-section__logoImage--2jkiD')]")