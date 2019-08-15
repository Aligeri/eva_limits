from selenium.webdriver.common.by import By


class NavigationLinks:
    password = (By.ID, "react-tabs-0")  # Вкладка password на странице Security
    emailConfirmation = (By.ID, "react-tabs-2")  # Вкладка email confirmation на странице Security
    twoFactorAuthentication = (By.ID, "react-tabs-4")  # Вкладка 2-factor authentication на странице Security
    pincode = (By.ID, "react-tabs-6")  # Вкладка pin-code на странице Security
    activeSessions = (By.ID, "react-tabs-8")  # Вкладка active sessions на странице Security
    limits = (By.ID, "react-tabs-10")  # Вкладка limits на странице Security


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
