from selenium.webdriver.common.by import By


class NavigationLinks:
    userDetails = (By.ID, "react-tabs-0")
    account = (By.ID, "react-tabs-2")
    importWallet = (By.ID, "react-tabs-4")
    exportWallet = (By.ID, "react-tabs-6")

class Account:
    emailNotifications = (By.XPATH, "//input[contains(@class, 'settings__input--oMx6t styles__input--2cyn3')]")
    dangerText = (By.XPATH, "//div[contains(@class, 'settings__dangerDescription--24GPv settings__description--3sdDL')]")
    successText = (By.XPATH, "//div[contains(@class, 'settings__successDescription--IowBh settings__description--3sdDL')]")