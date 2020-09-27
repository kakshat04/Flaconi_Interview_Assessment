from base.selenium_driver import SeleniumDriver as SD
from utility.custom_logging import custom_logger as cl
import logging


class PerfumeSelection(SD):
    log = cl(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # locators
    _parfum_tab_xpath = "//nav[@id='main-navigation']//a[@title='Parfum' and @href='/parfum/' and text()='Parfum']"
    _to_select_parfum_xpath = "//li[@id='80052967-C']"
    _cookies_accept_xpath = "//button[@id='uc-btn-accept-banner']"
    _search_box_xpath = "//form[@id='autosuggest-form-header']/input[2]"

    def accept_cookies(self):
        try:
            self.element_click(self._cookies_accept_xpath, "xpath")
        except Exception as Error:
            self.log.error(Error)

    def navigate_to_product(self, product):
        try:
            assert product.lower() == "parfum" or product.lower() == "perfume", f"Product Selected is {product}"
            self.element_click(self._parfum_tab_xpath, "xpath")
            return True
        except Exception as Error:
            self.log.error(Error)
            return False

    def select_perfume(self, perfume_name):
        try:
            assert perfume_name == "Tom Ford", f"Wrong Perfume name, Perfume name selected is {perfume_name}"
            self.element_click(self._to_select_parfum_xpath, "xpath")
            return True
        except Exception as Error:
            self.log.error(Error)

            # If selected perfume is not on the 1st page, enter Perfume name in search box
            try:
                self.enter_keys(self._search_box_xpath, "xpath", perfume_name)
                return True
            except Exception as error:
                self.log.error(error)
                return False








