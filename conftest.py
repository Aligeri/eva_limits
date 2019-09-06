import pytest
from selenium import webdriver
import os
import platform

global driver_screenshots
driver_screenshots = None
global url
server = "sanitarium"
url = r"https://app.%s.freewallet.org" % server
email_url = r"https://%s.freewallet.org" % server

# Фикстура для инициализации драйвера, возможно дописать выбор хром/хедлесс хром/фантомЖС из строки запуска
@pytest.mark.usefixtures("get_url")
@pytest.yield_fixture(scope="session")
def driver(request, get_url):
    options = webdriver.ChromeOptions()
    if platform.system() == "Linux":
        filepath = os.path.abspath(os.path.dirname(__file__))
        driverpath = os.path.join(filepath, "chromedriverLinux")
    if platform.system() == "Darwin":
        filepath = os.path.abspath(os.path.dirname(__file__))
        driverpath = os.path.join(filepath, "chromedriverMac")

    #options.add_argument('--start-maximized')
    #options.add_argument('--headless')
    #driverpath = "D:\FC\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driverpath, options=options)  # Временное решение, потом допилю подхват драйвера из PATH
    driver.maximize_window()
    global driver_screenshots
    if driver_screenshots == None:
        driver_screenshots = driver
    #driver.set_window_size(1920, 1080)
    driver.implicitly_wait(5)
    driver.get(get_url)
    yield driver
    driver.close()
    driver.quit()

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture(scope="function", autouse=True)
def screenshot(request):
    yield
    global driver_screenshots
    try:
        if request.node.rep_call.failed:
            take_screenshot(driver_screenshots, request.node.name)
    except AttributeError:
        if request.node.rep_setup.failed:
            take_screenshot(driver_screenshots, request.node.name)


# Фикстура для получения урла, на случай если урл мы будем получать извне (из CI например)
@pytest.fixture(scope='session', autouse=True)
def get_url(request):
    global url
    return url

def take_screenshot(driver, test_name):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'screenshots')
    screenshot_file_path = "{}/{}.png".format(filename, test_name)
    driver.save_screenshot(
        screenshot_file_path
    )


