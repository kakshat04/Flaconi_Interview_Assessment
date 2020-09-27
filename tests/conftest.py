import pytest
from selenium import webdriver
from Project.utility.send_email import EmailTest
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions


@pytest.yield_fixture(scope="class")
def oneTimeSetUp(request, browser):
    print("Running one time setUp")
    if browser == 'firefox':
        baseURL = "https://www.flaconi.de/"
        driver = webdriver.Firefox()
        driver.maximize_window()
        driver.implicitly_wait(3)
        driver.get(baseURL)
        print("Running tests on FF")
    else:
        baseURL = "https://www.flaconi.de/"
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--user-data-dir=chrome-data")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        driver.maximize_window()
        driver.implicitly_wait(3)
        driver.get(baseURL)
        print("Running tests on chrome")
    if request.cls is not None:
        request.cls.driver = driver

    yield driver
    driver.quit()
    sleep(1)
    print("Running one time tearDown")



def pytest_addoption(parser):
    parser.addoption("--browser")
    parser.addoption("--osType", help="Type of operating system")


@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def osType(request):
    return request.config.getoption("--osType")