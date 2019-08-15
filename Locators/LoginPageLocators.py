from selenium.webdriver.common.by import By


class MainPageLocators:
    signupButton = (By.XPATH, "//nav[@id='header']//a[contains(@class, 'btn btn-signup')]")
    loginButton = (By.XPATH, "//nav[@id='header']//a[text()='Login']")
    emailField = (By.NAME, 'email')


class LoginPageLocators:
    loginField = (By.NAME, 'email')
    passwordField = (By.NAME, 'password')
    repeatPasswordField= (By.NAME, 'passwordRepeat')
    loginButton = (By.XPATH, '//button[contains(@class, "button__button--2ccS0 auth__button--1I_62")]')
    incorrectPasswordTooltip = (By.CLASS_NAME, 'tippy-tooltip-content')
    signUpLink = (By.XPATH, "//a[text()='Sign up']")
    termsCheckbox = (By.XPATH, '//div[contains(text(), "I have read and accept")]')
    signUpButton = (By.XPATH, '//button[contains(@class, "button__button--2ccS0 auth__button--1I_62")]')

    facebook = (By.ID, "fb-login")
    facebookEmail = (By.NAME, "email")
    facebookPassword = (By.NAME, "pass")
    facebookLogin = (By.NAME, "login")
    facebookConfirm = (By.NAME, "__CONFIRM__")

    google = (By.ID, "google-login")
    googleEmail = (By.NAME, "identifier")
    googleEmailSubmit = (By.ID, "identifierNext")
    googlePassword = (By.NAME, "password")
    googlePasswordSubmit = (By.ID, "passwordNext")

    mobile = (By.ID, "mobile-login")


class Pincode:  # трешачина с фиксед позициями в xpath потому что нет айдишников
    create1 = (By.XPATH, "//h2[text()='Create 4-digit PIN code']/following-sibling::div[1]//input[1]")
    create2 = (By.XPATH, "//h2[text()='Create 4-digit PIN code']/following-sibling::div[1]//input[2]")
    create3 = (By.XPATH, "//h2[text()='Create 4-digit PIN code']/following-sibling::div[1]//input[3]")
    create4 = (By.XPATH, "//h2[text()='Create 4-digit PIN code']/following-sibling::div[1]//input[4]")

    repeat1 = (By.XPATH, "//h2[text()='Repeat']/following-sibling::div[1]//input[1]")
    repeat2 = (By.XPATH, "//h2[text()='Repeat']/following-sibling::div[1]//input[2]")
    repeat3 = (By.XPATH, "//h2[text()='Repeat']/following-sibling::div[1]//input[3]")
    repeat4 = (By.XPATH, "//h2[text()='Repeat']/following-sibling::div[1]//input[4]")

    login1 = (By.XPATH, "//div[@class = 'code-input__wrapperInput--34x8C']/input[1]")
    login2 = (By.XPATH, "//div[@class = 'code-input__wrapperInput--34x8C']/input[2]")
    login3 = (By.XPATH, "//div[@class = 'code-input__wrapperInput--34x8C']/input[3]")
    login4 = (By.XPATH, "//div[@class = 'code-input__wrapperInput--34x8C']/input[4]")
