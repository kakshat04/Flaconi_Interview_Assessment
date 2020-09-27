from time import sleep
from Project.base.selenium_driver import SeleniumDriver as SD
from Project.utility.custom_logging import custom_logger as cl
import logging


class LoginPage(SD):
    log = cl(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        # self.sd = SD(self.driver)

    # locators
    _email_field_name = "j_username"
    _password_field_name = "j_password"
    _login_button_xpath = "//button[contains(text(),'Login')]"
    _login_success_field_id = "tourWhatsNew"
    _login_failed_text_xpath = "//div[contains(text(),'This combination of email and password " \
                               "is not correct')]"

    def enter_email(self, email):
        # self.sd.enter_keys(self._email_field_id, 'id', email) # When done without Inheritance
        self.clear_text(self._email_field_name, 'name')
        self.enter_keys(self._email_field_name, 'name', email)

    def enter_password(self, pwd):
        # self.sd.enter_keys(self._password_field_id, 'id', pwd) # When done without Inheritance
        self.clear_text(self._password_field_name, 'name')
        self.enter_keys(self._password_field_name, 'name', pwd)

    def click_login_button(self):
        # self.sd.element_click(self._login_link, 'link') # When done without Inheritance
        self.element_click(self._login_button_xpath, 'xpath')

    def login_page(self, email='', password=''):
        print_msg = "Entering username & password.."
        print(print_msg)
        self.log.info(print_msg)
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()

    def verify_login_successful(self):
        # Clicking Dashboard, because of error in page
        # self.element_click("//span[contains(@class,'hideForSmall') and contains(text(),'Dashboard')]", "xpath")
        # sleep(1)
        is_login_success = self.is_element_present(self._login_success_field_id, 'id')
        if is_login_success:
            self.log.info("Login Successful...")
            print("Login Successful...")
            return True
        else:
            self.log.error("Login Failed...")
            print("Login Failed...")
            return False

    def verify_login_failed(self):
        is_login_fail = self.is_element_present(self._login_failed_text_xpath, 'xpath')
        if is_login_fail:
            self.log.info("Login Failed...")
            print("Login Failed...")
            return True
        else:
            self.log.error("Login successful with invalid Login..")
            print("Login successful with invalid Login..")
            return False



