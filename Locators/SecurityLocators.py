from selenium.webdriver.common.by import By


class NavigationLinks:
    password = (By.XPATH, "//li[contains(@class, 'security__tab--3spdg') and text()='Password']")  # Вкладка password на странице Security
    emailConfirmation = (By.XPATH, "//li[contains(@class, 'security__tab--3spdg') and text()='Email confirmation']")  # Вкладка email confirmation на странице Security
    twoFactorAuthentication = (By.XPATH, "//li[contains(@class, 'security__tab--3spdg') and text()='2-factor authentication']")  # Вкладка 2-factor authentication на странице Security
    pincode = (By.XPATH, "//li[contains(@class, 'security__tab--3spdg') and text()='PIN code']")  # Вкладка pin-code на странице Security
    activeSessions = (By.XPATH, "//li[contains(@class, 'security__tab--3spdg') and text()='Active sessions']")  # Вкладка active sessions на странице Security
    limits = (By.XPATH, "//li[contains(@class, 'security__tab--3spdg') and text()='Limits']")  # Вкладка limits на странице Security

class TwoFactorAuth:
    continueButton = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0 tab-two-fa__button--kwMkp')]")
    activationCode = (By.XPATH, "//p[@class='two-fa-activation__code--32OU4']")

    code1 = (By.XPATH, "//input[contains(@class, 'code-input__inputCode--eXUsf')][1]")
    code2 = (By.XPATH, "//input[contains(@class, 'code-input__inputCode--eXUsf')][2]")
    code3 = (By.XPATH, "//input[contains(@class, 'code-input__inputCode--eXUsf')][3]")
    code4 = (By.XPATH, "//input[contains(@class, 'code-input__inputCode--eXUsf')][4]")
    code5 = (By.XPATH, "//input[contains(@class, 'code-input__inputCode--eXUsf')][5]")
    code6 = (By.XPATH, "//input[contains(@class, 'code-input__inputCode--eXUsf')][6]")

    closeButton = (By.XPATH, "//button[contains(@class, 'tab-two-fa__closeButton--26DpQ')]")
    disable2fa = (By.XPATH, "//button[contains(@class, 'tab-two-fa__button--kwMkp')]")
    disableModal = (By.XPATH, '//button[contains(@class, "button__button--2ccS0 button__type-inline--3PR1T button__color-full-red--1bKJL")]')

    loginCheckboxState = (By.XPATH, "//div[@data-option='login']//input")
    payoutCheckboxState = (By.XPATH, "//div[@data-option='payout']//input")
    exportCheckboxState = (By.XPATH, "//div[@data-option='export']//input")

    loginCheckbox = (By.XPATH, "//div[@data-option='login']//label")
    payoutCheckbox = (By.XPATH, "//div[@data-option='payout']//label")
    exportCheckbox = (By.XPATH, "//div[@data-option='export']//label")

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
    doge = (By.XPATH, "//div[@class='item__limit--DH9Jj' and descendant::div[text()='Dogecoin wallet']]")

class LimitModal:
    amount = (By.NAME, "value")
    per24h = (By.XPATH, "//label[//input[@value='1']]")
    perWeek = (By.XPATH, "//label[//input[@value='7']]")
    setLimit = (By.XPATH, ".//button[@type='submit' and text()='Set limit']")
    cancel = (By.XPATH, ".//button[contains(@class, 'button__button--2ccS0') and text()='Cancel']")
    set = (By.XPATH, ".//button[contains(@class, 'button__button--2ccS0') and text()='Set']")
    activeLimit = (By.XPATH, "//div[contains(@class, 'detail__activeValue--1zKef')]")
    availableAmount = (By.XPATH, "//div[contains(@class, 'detail__periodValue--57-h6')]")
    pendingChange = (By.XPATH, "//div[contains(@class, 'detail__pendingTitle--1x3Cw')]")
    changeLimit = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0') and text()='Change limit']")
    disableLimit = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0') and text()='Disable']")
    disableLimitConfirm = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0 button__type-inline--3PR1T') and text()='Disable']")
    changeLimitConfirm = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0') and text()='Change']")
    overlay = (By.XPATH, ".//div[contains(@class, 'pp__popup--2rStv')]")
    BTCLimitPercent = (By.XPATH, "//div[text()='Bitcoin wallet']/following-sibling::div//span[contains(@class, 'item__percentLeft--2jVK3')]")
    DOGELimitPercent = (By.XPATH,
                       "//div[text()='Dogecoin wallet']/following-sibling::div//span[contains(@class, 'item__percentLeft--2jVK3')]")

    stats = (By.XPATH, "//div[contains(@class, 'security-stats__wrapper--eKhVI')]")

class Multisig:
    email1 = (By.XPATH, "//input[contains(@class, 'input__input--1lDmD tab-multisig__input--1ITcj')][1]")
    tooltip = (By.XPATH, "//div[contains(@class, 'simple-tooltip__tooltip--umHW1 simple-tooltip__error--1zX2v simple-tooltip__visible--2BGlS tab-multisig__tooltip--2gsKq')]")
    gotIt = (By.XPATH, "//a[text()='Got it']")
    stats = (By.XPATH, "//div[contains(@class, 'security-stats__wrapper--eKhVI')]")
    continueButton = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0 tab-multisig__saveButton--128q7')]")
    disclaimer = (By.XPATH, "//div[contains(@class, 'tab-multisig__disclaimerWithChild--2DkfO')]")
    disclaimerDiscard = (By.XPATH, "//a[contains(@class, 'tab-multisig__disclaimerCancelPending--2a7Ip')]")
    disclaimerDisable = (By.XPATH, "//a[contains(@class, 'tab-multisig__disclaimerDisableAll--2RjWV')]")
    confirmedAddressFirst = (By.XPATH, "//div[contains(@class, 'tab-multisig__confirmedEmailItem--3LH85')]")
    pending_multisig_status = (By.XPATH, "//div[contains(@class, 'multisig__pendingEmailItemStatus')]")
    disclaimer_title = (By.XPATH, "//h2[contains(@class, 'disclaimer__title--3-6C7')]")

class Password:
    password = (By.XPATH, "//input[@name='password']")
    newPassword = (By.XPATH, "//input[@name='newPassword']")
    newPasswordRepeat = (By.XPATH, "//input[@name='newPasswordRepeat']")
    savePassword = (By.XPATH, "//button[contains(@class, 'security__saveButton--1NeUP')]")
    tooltip = (By.XPATH, "//div[@data-original-title='Password changed successfully!']")

class ActiveSessions:
    sessionBlock = (By.XPATH, "//div[contains(@class, 'tab-sessions__session--1CVnR')]")
    singleSessionDrop = (By.XPATH, "//button[contains(@class, 'tab-sessions__dropButton--1A65y')]")
    sessionBody = (By.XPATH, "//div[contains(@class, 'tab-sessions__model--3RUWz')]")
    sessionPlatform = (By.XPATH, "//div[contains(@class, 'tab-sessions__platformTitle--1CSBr')]")
    allSessionsDrop = (By.XPATH, "//button[contains(@class, 'tab-sessions__button--6zMwa')]")
    dropYes = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0') and text()='Yes']")
    dropClose = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0') and text()='Close']")
