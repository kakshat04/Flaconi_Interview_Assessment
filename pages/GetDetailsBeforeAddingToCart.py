from base.selenium_driver import SeleniumDriver as SD
from utility.custom_logging import custom_logger as cl
import logging


class DetailBeforeAdditionToCart(SD):
    log = cl(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        # self.sd = SD(self.driver)

    # locators
    _before_cart_perfume_name_xpath = "//div[@class='product-name' and contains(text(),'Tom Ford')]"
    _before_cart_perfume_size_xpath = "//div[@id='htmlData']//div[3]/span[1]"
    _before_cart_perfume_unit_xpath = "//div[@id='htmlData']//div[3]/span[2]"
    _before_cart_perfume_price_xpath = "//div[@id='htmlData']//div[2]/span[1]"
    _add_cart_button_xpath = "//a[text()='Zum Warenkorb']"

    def get_detail_before_adding_cart(self):
        # Perfume name
        name = self.get_element_text(self._before_cart_perfume_name_xpath, "xpath")[:8]
        # Perfume Size.text
        size = self.get_element_text(self._before_cart_perfume_size_xpath, "xpath")
        unit = self.get_element_text(self._before_cart_perfume_unit_xpath, "xpath")
        # Perfume Price.text
        price = self.get_element_text(self._before_cart_perfume_price_xpath, "xpath")[:-1]

        details = [name, size, unit, price]
        print(f"Perfume Details :: {details}")
        self.log.info(f"Perfume Details :: {details}")
        return details

    def proceed_with_selection(self):
        self.element_click(self._add_cart_button_xpath, "xpath")
