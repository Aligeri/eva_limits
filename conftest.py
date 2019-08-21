import pytest
from selenium import webdriver
import os


global url
url = r"https://app.sanitarium.freewallet.org/"

# Фикстура для инициализации драйвера, возможно дописать выбор хром/хедлесс хром/фантомЖС из строки запуска
@pytest.mark.usefixtures("get_url")
@pytest.yield_fixture(scope="session")
def driver(request, get_url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    filepath = os.path.abspath(os.path.dirname(__file__))
    driverpath = os.path.join(filepath, "chromedriver")
    #driverpath = "D:\FC\chromedriver.exe"
    global driver
    driver = webdriver.Chrome(executable_path=driverpath, options=options)  # Временное решение, потом допилю подхват драйвера из PATH
    driver.set_window_size(1920, 1080)
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
    if request.node.rep_call.failed:
        global driver
        take_screenshot(driver, request.node.name)


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


