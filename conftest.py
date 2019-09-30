import pytest
from selenium import webdriver
import os
import platform
from Pages.BasePage import Page

global driver_screenshots
driver_screenshots = None
global url
global testexec
global xrayconf
xrayconf = None

server = "sanitarium"
url = r"https://app.%s.freewallet.org" % server
email_url = r"https://%s.freewallet.org" % server

pytest_plugins = "xrayplugin.conftest"

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
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
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
    report = outcome.get_result()
    setattr(item, "report_" + report.when, report)
    return report

@pytest.fixture(scope='function', autouse=True)
def data_logout(driver):
    base_page = Page(driver)
    base_page.reset_session()
    yield

@pytest.fixture(scope="function", autouse=True)
@pytest.mark.usefixtures("driver")
def screenshot(request, driver):
    yield
    global driver_screenshots
    try:
        if request.node.report_call.failed:
            take_screenshot(driver_screenshots, request.node.name)
            take_report(driver_screenshots, request.node.name, str(request.node.report_call.longrepr))
    except AttributeError:
        if request.node.report_setup.failed:
            take_screenshot(driver_screenshots, request.node.name)
            take_report(driver_screenshots, request.node.name, str(request.node.report_call.longrepr))


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

def take_report(driver, test_name, report):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'screenshots')
    report_file_path = "{}/{}.txt".format(filename, test_name)
    file = open(report_file_path, "w+")
    file.write(report)



