from base.selenium_driver import SeleniumDriver as SD
from utility.custom_logging import custom_logger as cl
import logging


class PerfumeDetailsFromCart(SD):
    log = cl(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.final_values = {}
        # self.sd = SD(self.driver)

    # locators
    _after_cart_perfume_name_xpath = "//div[@class='details']//a[contains(text(),'Tom Ford')]"
    _after_cart_perfume_price_xpath = "//span[@class='price-sale']"
    _selected_perfume_number_dd_xpath = "//select[@id='cartQuantity80052967-50']"
    _main_page_navigator = "//a[@class='logo-image']"

    def get_perfume_detail_from_cart(self):
        # Make sure selected item is 1 in number
        if self.get_element_text(self._selected_perfume_number_dd_xpath, "xpath") != "1":
            self.select_from_dropdown(self._selected_perfume_number_dd_xpath, "xpath", "1")

        # Verify perfume name and price - if wrong, fail the test case
        name = self.get_element_text(self._after_cart_perfume_name_xpath, "xpath")[:8]

        element = self.get_element(".details", "css")
        javascript_command = """
          return Array.from(arguments[0].childNodes)
            .filter(function(o){return o.nodeType === 3 && o.nodeValue.trim().length;})
            .map(function(o){return o.nodeValue.trim();})
          """
        after_cart_perfume_size_unit = self.execute_javascript(javascript_command, element)
        after_cart_perfume_details = after_cart_perfume_size_unit[0].split(" ")
        size = after_cart_perfume_details[-2]
        unit = after_cart_perfume_details[-1]

        price = self.get_element_text(self._after_cart_perfume_price_xpath, "xpath")

        details = [name, size, unit, price]
        print(f"Perfume Details :: {details}")

        return details

    def navigate_to_main_page(self):
        self.element_click(self._main_page_navigator, "xpath")


