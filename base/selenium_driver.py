from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains
from Project.utility.custom_logging import custom_logger as cl
import logging
import pyperclip


class SeleniumDriver:
    log = cl(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def get_by_type(self, locator_type):
        locator_type = locator_type.lower()
        if locator_type == 'id':
            return By.ID
        elif locator_type == 'name':
            return By.NAME
        elif locator_type == 'class':
            return By.CLASS_NAME
        elif locator_type == 'link':
            return By.LINK_TEXT
        elif locator_type == 'xpath':
            return By.XPATH
        elif locator_type == 'css':
            return By.CSS_SELECTOR
        elif locator_type == 'tag':
            return By.TAG_NAME
        else:
            return "Invalid Locator Type Entered \n Locator type should be in [id, name, class, link, xpath, css, tag]"

    def get_element(self, locator, locator_type):
        element = None
        try:
            by_type = self.get_by_type(locator_type)
            element = self.driver.find_element(by_type, locator)
            self.log.info("Element found with locator: " + locator + " and locator type: " + locator_type)
        except:
            self.log.error("Element not found with locator: " + locator + " and locator type: " + locator_type)
        return element

    def get_elements(self, locator, locator_type):
        element = None
        try:
            by_type = self.get_by_type(locator_type)
            element = self.driver.find_elements(by_type, locator)
            self.log.info("Elements found with locator: " + locator + " and locator type: " + locator_type)
        except:
            self.log.error("Elements not found with locator: " + locator + " and locator type: " + locator_type)
        return element

    def is_element_present(self, locator, locator_type):
        try:
            element = self.get_element(locator, locator_type)
            if element is not None:
                self.log.info("Element Present on the web page")
                return True
            else:
                self.log.error("Element is not present on the web page")
                return False
        except:
            self.log.error("Element is not present on the web page")
            return False

    def element_click(self, locator, locator_type):
        element = None
        try:
            element = self.get_element(locator, locator_type)
            element.click()
            self.log.info("Element click successful with locator: " + locator +
                          " and locator type: " + locator_type)
        except:
            self.log.error("Element click not successful with locator: " + locator +
                           " and locator type: " + locator_type)
        return element

    def enter_keys(self, locator, locator_type, text):
        element = None
        try:
            element = self.get_element(locator, locator_type)
            element.send_keys(text)
            self.log.info("Element send keys successful with locator: " + locator +
                          " and locator type: " + locator_type)
        except:
             self.log.error("Element send keys not successful with locator: " + locator +
                            " and locator type: " + locator_type)
        return element

    def wait_for_element(self, locator, locator_type):
        element = None
        try:
            by_type = self.get_by_type(locator_type)
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException,
                                                     StaleElementReferenceException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable(by_type, locator))
            self.log.info("Element wait successful with locator: " + locator +
                          " and locator type: " + locator_type)
        except:
            self.log.error("Element wait not successful with locator: " + locator +
                           " and locator type: " + locator_type)
        return element

    def clear_text(self, locator, locator_type):
        try:
            element = self.get_element(locator, locator_type)
            element.clear()
            self.log.info("Element clear text successful with locator: " + locator +
                          " and locator type: " + locator_type)
        except:
            self.log.error("Element clear text not successful with locator: " + locator +
                           " and locator type: " + locator_type)

    def scroll_to(self, locator, locator_type):
        try:
            element = self.get_element(locator_type, locator_type)
            element.location_once_scrolled_into_view

            self.log.info("Element scroll successful with locator: " + locator +
                          " and locator type: " + locator_type)
        except:
            self.log.error("Element scroll not successful with locator: " + locator +
                           " and locator type: " + locator_type)

    def execute_javascript(self, command):
        try:
            self.driver.execute_script(command)
            self.log.info("Java Script ran successfully with command" + command)
        except:
            self.log.error("Java Script failed with command" + command)

    def get_page_title(self):
        return self.driver.title

    def switch_to_frame(self, frame=0):
        try:
            self.driver.switch_to.frame(frame)
            self.log.info("Frame switched Successfully")
        except:
            self.log.error("Frame not switched successfully")

    def switch_to_original_frame(self):
        try:
            self.driver.switch_to.default_content()
            self.log.info("Frame Switched to Original")
        except:
            self.log.error("Frame not switched to Original")

    def submit(self, locator, locator_type, text):
        try:
            element = self.enter_keys(locator, locator_type, text)
            element.send_keys(Keys.ENTER)
            self.log.info("Element send keys successful with locator: " + locator +
                          " and locator type: " + locator_type)
        except:
             self.log.error("Element send keys not successful with locator: " + locator +
                            " and locator type: " + locator_type)

    def get_attribute(self, locator, locator_type, attribute_name):
        attribute = None
        try:
            element = self.get_element(locator, locator_type)
            attribute = element.get_attribute(attribute_name)
            self.log.info("Get Attribute successful with locator: " + locator +
                          " and locator type: " + locator_type)
        except:
            self.log.error("Get Attribute not successful with locator: " + locator +
                           " and locator type: " + locator_type)

        return attribute

    def perform_action_chains(self, locator, locator_type, action):
        element = None
        try:
            element = self.get_element(locator, locator_type)
            ActionChains(self.driver).move_to_element(element).perform()
            if action == "click":
                element.click()
            self.log.info("Action Chain successful with locator: " + locator +
                          " and locator type: " + locator_type)
        except:
            self.log.error("Action Chain not successful with locator: " + locator +
                           " and locator type: " + locator_type)
        return element

    def get_element_text(self, locator, locator_type):
        text = None
        try:
            element = self.get_element(locator, locator_type)
            text = element.text
            self.log.info("Text Found successful with locator: " + locator +
                          " and locator type: " + locator_type)
        except:
            self.log.error("Text Found not successful with locator: " + locator +
                           " and locator type: " + locator_type)
        return text

    def enter_text_in_textarea(self, locator, locator_type, text):
        try:
            element = self.get_element(locator, locator_type)
            element.send_keys(Keys.CONTROL + 'a')
            element.send_keys(Keys.DELETE)
            # element.send_keys(text)  # This is taking lot of time to enter complete text
            pyperclip.copy(text)  # Copy text to clipboard
            element.send_keys(Keys.CONTROL + 'v')
            self.log.info("Text Found successful with locator: " + locator +
                          " and locator type: " + locator_type)
        except:
            self.log.error("Text Found not successful with locator: " + locator +
                           " and locator type: " + locator_type)

    def is_element_enabled(self, locator, locator_type):
        element = self.get_element(locator, locator_type)
        button_status = element.is_enabled()
        if button_status:
            self.log.info("Button is enabled..")
            return True
        else:
            self.log.info("Button is not enabled..")
            return False








