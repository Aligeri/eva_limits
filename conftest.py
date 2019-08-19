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
    #options.add_argument('--headless')
    filepath = os.path.abspath(os.path.dirname(__file__))
    driverpath = os.path.join(filepath, "chromedriver")
    driver = webdriver.Chrome(executable_path=driverpath, options=options)  # Временное решение, потом допилю подхват драйвера из PATH
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(5)
    driver.get(get_url)
    failed_tests = request.session.testsfailed
    yield driver
    if request.session.testsfailed != failed_tests:
        test_name = request.node.name
        take_screenshot(driver, test_name)
    driver.quit()


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


