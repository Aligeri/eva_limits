import pytest
from selenium import webdriver
import os

# Фикстура для инициализации драйвера, возможно дописать выбор хром/хедлесс хром/фантомЖС из строки запуска
@pytest.mark.usefixtures("url")
@pytest.yield_fixture(scope="function")
def driver(request, url):
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=r"/home/user/Downloads/chromedriver", options=options)
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(10)
    driver.get(url)
    failed_tests = request.session.testsfailed
    yield driver
    if request.session.testsfailed != failed_tests:
        test_name = request.node.name
        take_screenshot(driver, test_name)
    driver.quit()


# Фикстура для получения урла, на случай если урл мы будем получать извне (из CI например)
@pytest.fixture(scope='session', autouse=True)
def url(request):
    return r"https://app.sanitarium.freewallet.org/"

def take_screenshot(driver, test_name):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'screenshots')
    screenshot_file_path = "{}/{}.png".format(filename, test_name)
    driver.save_screenshot(
        screenshot_file_path
    )
