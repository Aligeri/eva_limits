from selenium.webdriver.common.by import By

class AdminTransSearchLocators:
    transactionID = By.XPATH("//input[@placeholder = 'Transaction ID']")
    submitButton = By.XPATH("//button[@type='submit']")

class AdminTransTableLocators:
    moreButton = By.XPATH("//span[@class='caret']")
    approveButton = By.XPATH("//a[text()='Approve']")
    disapproveButton = By.XPATH("//a[text()='Disapprove']")