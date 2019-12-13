from selenium.webdriver.common.by import By


class NavigationLinks:
    userDetails = (By.XPATH, "//li[contains(@class, 'settings__tab--7oBOJ') and text()='User details']")
    account = (By.XPATH, "//li[contains(@class, 'settings__tab--7oBOJ') and text()='Account']")
    importWallet = (By.XPATH, "//li[contains(@class, 'settings__tab--7oBOJ') and text()='Import wallet']")
    exportWallet = (By.XPATH, "//li[contains(@class, 'settings__tab--7oBOJ') and text()='Export wallet']")
    mnemonic = (By.XPATH, "//li[contains(@class, 'settings__tab--7oBOJ') and text()='Mnemonic phrase']")
    privateKey = (By.XPATH, "//li[contains(@class, 'settings__tab--7oBOJ') and text()='Private key']")
    identity = (By.XPATH, "//li[contains(@class, 'settings__tab--7oBOJ') and text()='Identity']")

class Account:
    emailNotifications = (By.XPATH, "//input[contains(@class, 'settings__input--oMx6t styles__input--2cyn3')]")
    dangerText = (By.XPATH, "//div[contains(@class, 'settings__dangerDescription--24GPv settings__description--3sdDL')]")
    successText = (By.XPATH, "//div[contains(@class, 'settings__successDescription--IowBh settings__description--3sdDL')]")
    SaveBtn = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0 settings__button--11kwP button__type-inline--3PR1T')]")
    VerificationPopup = (By.XPATH, "//div[contains(@class, 'pp__popup--2rStv settings__verificationPopup--28NHV')]")
    SendLinkBtn = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0') and text()='Send link']")
    ResendLink = (By.XPATH, "//a[@class='settings__resendLink--CVBaW']")
    ConfirmEmailText = (By.XPATH, "//div[contains(@class, 'settings__warningDescription--Oh3AO settings__description--3sdDL') and text()='Confirm email change']")

    languageDropdown = (By.XPATH, '//div[text()="Language"]/div')
    languageEn = (By.XPATH, "//option[@value='en']")
    languageJa = (By.XPATH, "//option[@value='ja']")
    languageRu = (By.XPATH, "//option[@value='ru']")

class FiatCurrency:
    fiatCurrencyDropdown = (By.XPATH, "//select[@id='local-currency']")
    fiatUsd = (By.XPATH, "//option[@value='usd']")
    fiatEur = (By.XPATH, "//option[@value='eur']")
    fiatGbp = (By.XPATH, "//option[@value='gbp']")
    fiatRub = (By.XPATH, "//option[@value='rub']")

class userDetails:
    Name = (By.XPATH, "//input[@placeholder='Name']")
    UserId = (By.XPATH, "//input[@placeholder='User ID']")
    SaveBtn = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0 settings__saveButton--1VzwW')]")

class Identity:
    Badge = (By.XPATH, "//div[contains(@class, 'badge__badge--D7Fy- badge__red--zTfOo settings__badge--SmlrG')]")
    firstName = (By.XPATH, "//input[@name='name']")
    firstNameError = (By.XPATH, "//input[@name='name']/following-sibling::div")
    secondName = (By.XPATH, "//input[@name='surname']")
    secondNameError = (By.XPATH, "//input[@name='surname']/following-sibling::div")
    birthDate = (By.XPATH, "//input[@name='birthday']")
    birthDateError = (By.XPATH, "//input[@name='birthday']/following-sibling::div")
    identityFrontFile = (By.XPATH, ".//input[@name='identity[0]']")
    identityFrontFileError = (By.XPATH, ".//input[@name='identity[0]']/following-sibling::div")
    identityBackFile = (By.XPATH, ".//input[@name='identity[1]']")
    identityBackFileError = (By.XPATH, ".//input[@name='identity[1]']/following-sibling::div")
    identityFrontFileName = (By.XPATH, ".//input[@name='identity[0]']/following-sibling::span[contains(@class, 'input-image__name--2A6q9')]")
    identityBackFileName = (By.XPATH, ".//input[@name='identity[1]']/following-sibling::span[contains(@class, 'input-image__name--2A6q9')]")
    selfieFile = (By.XPATH, "//input[@name='selfie']")
    selfieFileError = (By.XPATH, "//input[@name='selfie']/following-sibling::div")
    selfieFileName = (By.XPATH, "//input[@name='selfie']/following-sibling::span[contains(@class, 'input-image__name--2A6q9')]")
    submit = (By.XPATH, "//button[contains(@class, 'tab-kyc__submit--18iGh')]")


class Mnemonic:
    gotIt = (By.XPATH, ".//a[@class='settings__tooltipAction--3DkWd' and text()='Got it']")
    generate = (By.XPATH, ".//button[text()='Generate']")
    mouseArea = (By.XPATH, "//div[@class='generate__mousedArea--2njVs']")
    percent = (By.XPATH, "//div[@class='generate__percentArea--2T3j8']")
    continueButton = (By.XPATH, ".//button[contains(@class, 'button__button--2ccS0') and text()='Continue']")
    mnemonicKey = (By.XPATH, "//div[contains(@class, 'mnemonic__mmKeys--9eBtJ')]")
    thirdWordInput = (By.XPATH, "//input[@class='input__input--1lDmD']")
    finishButton = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0') and text()='Finish']")
    publicKey = (By.XPATH, "//p[@class='private-key__code--2H_to'][1]")
    privateKey = (By.XPATH, "//p[@class='private-key__code--2H_to'][2]")
    storedCheckbox = (By.XPATH, "//div[@class='checkbox__text--29Pay']")