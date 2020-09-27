from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from utility.custom_logging import custom_logger as cl
import logging
import time


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

    def element_click(self, locator, locator_type):
        element = None
        try:
            element = self.get_element(locator, locator_type)
            element.click()
            time.sleep(5)
            self.log.info("Element click successful with locator: " + locator +
                          " and locator type: " + locator_type)
        except:
            self.log.error("Element click not successful with locator: " + locator +
                           " and locator type: " + locator_type)
        return element

    def execute_javascript(self, command, element):
        try:
            return self.driver.execute_script(command, element)
            self.log.info("Java Script ran successfully with command" + command)
        except:
            self.log.error("Java Script failed with command" + command)

    def get_page_title(self):
        return self.driver.title

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

    def select_from_dropdown(self, locator, locator_type, value):
        try:
            element = self.get_element(locator, locator_type)
            select = Select(element)
            select.select_by_visible_text(value)
            time.sleep(3)
            self.log.info("Element selection successful with locator: " + locator +
                          " and locator type: " + locator_type)
        except:
            self.log.error("Element selection not successful with locator: " + locator +
                           " and locator type: " + locator_type)

    def enter_keys(self, locator, locator_type, text):
        element = None
        try:
            element = self.get_element(locator, locator_type)
            element.send_keys(text)
            element.submit()
            self.log.info("Element send keys successful with locator: " + locator +
                          " and locator type: " + locator_type)
        except Exception as error:
            self.log.error("Element send keys not successful with locator: " + locator +
                           " and locator type: " + error)
        return element



