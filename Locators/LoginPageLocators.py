from selenium.webdriver.common.by import By


class MainPageLocators:
    signupButton = (By.XPATH, "//nav[@id='header']//a[contains(@class, 'btn btn-signup')]")
    loginButton = (By.XPATH, "//nav[@id='header']//a[text()='Login']")
    emailField = (By.NAME, 'email')


class LoginPageLocators:
    loginField = (By.NAME, 'email')  # Поле email на странице логина и регистрации
    passwordField = (By.NAME, 'password')  # Поле пароля на странице логина и регистрации
    repeatPasswordField= (By.NAME, 'passwordRepeat')  # Поле повтора пароля на странице регистрации
    loginButton = (By.XPATH, '//button[contains(@class, "button__button--2ccS0 auth__button--1I_62")]')  # Кнопка логина на странице авторизации
    incorrectPasswordTooltip = (By.CLASS_NAME, 'tippy-tooltip-content')  # Тултип с предупреждением на странице авторизации
    pincodeTooltip = (By.XPATH, "//div[contains(@class, 'auth__tooltip--3kgfI')]")
    signUpLink = (By.XPATH, "//a[text()='Sign up']")  # Кнопка sign up на странице авторизации
    termsCheckbox = (By.XPATH, '//div[contains(text(), "I have read and accept")]')  # Обязательный чекбокс на странице регистрации
    signUpButton = (By.XPATH, '//button[contains(@class, "button__button--2ccS0 auth__button--1I_62")]')  # Кнопка sign up на странице регистрации

    facebook = (By.ID, "fb-login")  # Кнопка facebook на страницах авторизации и регистрации
    facebookEmail = (By.NAME, "email")  # Поле email в поп-апе фейсбука
    facebookPassword = (By.NAME, "pass")  # Поле password в поп-апе фейсбука
    facebookLogin = (By.NAME, "login")  # Кнопка login в поп-апе фейсбука
    facebookConfirm = (By.NAME, "__CONFIRM__")  # Кнопка confirm при регистрации с фейсбуком

    google = (By.ID, "google-login")  # Кнопка google на страницах регистрации и авторизации
    googleEmail = (By.XPATH, "//input[@type='email']")  # Поле email в поп-апе гугла
    googleEmailSubmit = (By.ID, "identifierNext")  # Кнопка подтверждения емейла в поп-апе гугла
    googlePassword = (By.XPATH, "//input[@type='password']")  # Поле пароля в поп-апе гугла
    googlePasswordSubmit = (By.ID, "passwordNext")  # Кнопка подтверждения пароля в поп-апе гугла
    googleChangeAddress = (By.XPATH, "//div[contains(@class, 'BHzsHc')]|//a[@id='account-chooser-add-account']")
    totp = (By.ID, "totpPin")
    totpSubmit = (By.XPATH, "//span[contains(@class, 'RveJvd snByac')]|//input[contains(@class, 'MK9CEd MVpUfe')]")
    googlePopup = (By.CLASS_NAME, "zWl5kd")

    mobile = (By.ID, "mobile-login")  # Кнопка mobile на страницах авторизации и регистрации

    logoutLink = (By.XPATH, "//a[contains(@class, 'header__logoutLink--uc90u header__link--1ckAu')]")
    logoutButton = (By.XPATH, "//button[contains(@class, 'button__button--2ccS0') and text()='Logout']")

    lockPopup = (By.XPATH, "//div[contains(@class, 'pp__popup--2rStv user-blocked-popup__popup--yksZo')]")
    lockPopupBody = (By.XPATH, "//div[contains(@class, 'pp__body--3MhWo')]")

class Pincode:  # трешачина с фиксед позициями в xpath потому что нет айдишников
    title = (By.XPATH, "//h1[contains(@class, 'auth__title--1GAPf') and text()='PIN code']")

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
