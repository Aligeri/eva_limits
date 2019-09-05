from selenium.webdriver.common.by import By

class UsersSelectors:
    usersDropdown = (By.XPATH, "//span[text()='Users']")
    usersSearch = (By.XPATH, "//a[text()='Search']")
    usersBlocked = (By.XPATH, "//a[text()='Blocked']")

class TransactionsSelectors:
    transDropdown = (By.XPATH, "//span[text()='Transactions']")
    transList = (By.XPATH, "//a[text()='List']")
    transDashboard = (By.XPATH, "//a[text()='Dashboard']")
    transPool = (By.XPATH, "//a[text()='Pool search']")
    transLimits = (By.XPATH, "//a[text()='Payout limits']")
