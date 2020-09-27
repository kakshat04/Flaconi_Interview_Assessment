import pytest
from selenium import webdriver
from Project.utility.send_email import EmailTest
from time import sleep


@pytest.yield_fixture(scope="class")
def oneTimeSetUp(request, browser):
    print("Running one time setUp")
    if browser == 'firefox':
        baseURL = "https://demo-eu.leanix.net/akkDemo/ "
        driver = webdriver.Firefox()
        driver.maximize_window()
        driver.implicitly_wait(3)
        driver.get(baseURL)
        print("Running tests on FF")
    else:
        baseURL = "https://demo-eu.leanix.net/akkDemo/"
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.implicitly_wait(3)
        driver.get(baseURL)
        print("Running tests on chrome")

    if request.cls is not None:
        request.cls.driver = driver

    yield driver
    # driver.quit()
    sleep(1)
    # Send email with Report attachment
    recipient = 'kumar.akshat04@gmail.com'
    subject = 'Test Email'
    body = 'Execution Report'
    report_path = r'F:\LeanIX_Assessment\Report.html'
    # print("----------- Inside Email section ------------")
    # email = EmailTest(recipient, subject, body, report_path)
    # email.send_email()
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