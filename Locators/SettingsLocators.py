from selenium.webdriver.common.by import By


class NavigationLinks:
    userDetails = (By.XPATH, "//li[contains(@class, 'settings__tab--7oBOJ') and text()='User details']")
    account = (By.XPATH, "//li[contains(@class, 'settings__tab--7oBOJ') and text()='Account']")
    importWallet = (By.XPATH, "//li[contains(@class, 'settings__tab--7oBOJ') and text()='Import wallet']")
    exportWallet = (By.XPATH, "//li[contains(@class, 'settings__tab--7oBOJ') and text()='Export wallet']")
    mnemonic = (By.XPATH, "//li[contains(@class, 'settings__tab--7oBOJ') and text()='Mnemonic phrase']")
    privateKey = (By.XPATH, "//li[contains(@class, 'settings__tab--7oBOJ') and text()='Private key']")

class Account:
    emailNotifications = (By.XPATH, "//input[contains(@class, 'settings__input--oMx6t styles__input--2cyn3')]")
    dangerText = (By.XPATH, "//div[contains(@class, 'settings__dangerDescription--24GPv settings__description--3sdDL')]")
    successText = (By.XPATH, "//div[contains(@class, 'settings__successDescription--IowBh settings__description--3sdDL')]")

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