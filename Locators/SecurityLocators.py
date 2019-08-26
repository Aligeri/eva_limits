from selenium.webdriver.common.by import By


class NavigationLinks:
    password = (By.XPATH, "//li[contains(@class, 'security__tab--3spdg') and text()='Password']")  # Вкладка password на странице Security
    emailConfirmation = (By.XPATH, "//li[contains(@class, 'security__tab--3spdg') and text()='Email confirmation']")  # Вкладка email confirmation на странице Security
    twoFactorAuthentication = (By.XPATH, "//li[contains(@class, 'security__tab--3spdg') and text()='2-factor authentication']")  # Вкладка 2-factor authentication на странице Security
    pincode = (By.XPATH, "//li[contains(@class, 'security__tab--3spdg') and text()='PIN code']")  # Вкладка pin-code на странице Security
    activeSessions = (By.XPATH, "//li[contains(@class, 'security__tab--3spdg') and text()='Active sessions']")  # Вкладка active sessions на странице Security
    limits = (By.XPATH, "//li[contains(@class, 'security__tab--3spdg') and text()='Limits']")  # Вкладка limits на странице Security


class SecurityPincode:
    current1 = (
        By.XPATH,
        "//div[text()='Please enter your current PIN code to make changes']/following-sibling::div[1]//input[1]")
    current2 = (
        By.XPATH,
        "//div[text()='Please enter your current PIN code to make changes']/following-sibling::div[1]//input[2]")
    current3 = (
        By.XPATH,
        "//div[text()='Please enter your current PIN code to make changes']/following-sibling::div[1]//input[3]")
    current4 = (
        By.XPATH,
        "//div[text()='Please enter your current PIN code to make changes']/following-sibling::div[1]//input[4]")

    new1 = (By.XPATH, "//div[text()='Enter new PIN code']/following-sibling::div[1]//input[1]")
    new2 = (By.XPATH, "//div[text()='Enter new PIN code']/following-sibling::div[1]//input[2]")
    new3 = (By.XPATH, "//div[text()='Enter new PIN code']/following-sibling::div[1]//input[3]")
    new4 = (By.XPATH, "//div[text()='Enter new PIN code']/following-sibling::div[1]//input[4]")

    repeat1 = (By.XPATH, "//div[text()='Repeat']/following-sibling::div[1]//input[1]")
    repeat2 = (By.XPATH, "//div[text()='Repeat']/following-sibling::div[1]//input[2]")
    repeat3 = (By.XPATH, "//div[text()='Repeat']/following-sibling::div[1]//input[3]")
    repeat4 = (By.XPATH, "//div[text()='Repeat']/following-sibling::div[1]//input[4]")

    successPopup = (By.XPATH, "//div[contains(@class, 'pp__popup--2rStv tab-pin__successPopup--1X0uA')]")

class LimitWallets:
    fwt = (By.XPATH, "//div[@class='item__limit--DH9Jj' and descendant::div[text()='FWT wallet']]")
    ardr = (By.XPATH, "//div[@class='item__limit--DH9Jj' and descendant::div[text()='Ardor wallet']]")
    btc = (By.XPATH, "//div[@class='item__limit--DH9Jj' and descendant::div[text()='Bitcoin wallet']]")

class LimitModal:
    amount = (By.NAME, "value")
    per24h = (By.XPATH, "//label[//input[@value='1']]")
    perWeek = (By.XPATH, "//label[//input[@value='7']]")
    setLimit = (By.XPATH, "//button[@type='submit' and text()='Set limit']")
    cancel = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0 button__type-inline--3PR1T') and text()='Cancel']")
    set = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0 button__type-inline--3PR1T') and text()='Set']")
    activeLimit = (By.XPATH, "//div[contains(@class, 'detail__activeValue--1zKef')]")
    availableAmount = (By.XPATH, "//div[contains(@class, 'detail__periodValue--57-h6')]")
    pendingChange = (By.XPATH, "//div[contains(@class, 'detail__pendingTitle--1x3Cw')]")
    changeLimit = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0') and text()='Change limit']")
    disableLimit = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0') and text()='Disable']")
    disableLimitConfirm = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0 button__type-inline--3PR1T') and text()='Disable']")
    changeLimitConfirm = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0') and text()='Change']")
    overlay = (By.XPATH, "//div[@class = 'pp__overlay--3alEV']")
    BTCLimitPercent = (By.XPATH, "//div[text()='Bitcoin wallet']/following-sibling::div//span[contains(@class, 'item__percentLeft--2jVK3')]")

class Multisig:
    email1 = (By.XPATH, "//input[contains(@class, 'input__input--1lDmD tab-multisig__input--1ITcj')][1]")
    tooltip = (By.XPATH, "//div[contains(@class, 'simple-tooltip__tooltip--umHW1 simple-tooltip__error--1zX2v simple-tooltip__visible--2BGlS tab-multisig__tooltip--2gsKq')]")
    gotIt = (By.XPATH, "//a[contains(@class, 'tab-multisig__tooltipAction---Ts24')]")
    continueButton = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0 tab-multisig__saveButton--128q7')]")
    disclaimer = (By.XPATH, "//div[contains(@class, 'tab-multisig__disclaimerWithChild--2DkfO')]")
    disclaimerDiscard = (By.XPATH, "//a[contains(@class, 'tab-multisig__disclaimerCancelPending--2a7Ip')]")