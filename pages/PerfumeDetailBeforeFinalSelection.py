from base.selenium_driver import SeleniumDriver as SD
from utility.custom_logging import custom_logger as cl
import logging


class SelectPerfumeToAddToCart(SD):
    log = cl(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # locators
    _selected_parfum_name_xpath = "//a[@title='Mehr von Tom Ford' and @class='brand']"
    _selected_parfum_size_num_xpath = "//li[@id='product-sku-80052967-50']/div/div[2]/span[1]"
    _selected_parfum_size_unit_xpath = "//li[@id='product-sku-80052967-50']/div/div[2]/span[2]"
    _selected_parfum_price_xpath = "//li[@id='product-sku-80052967-50']/div/div[3]/span[1]"
    _perfume_select_button_xpath = "//form[@id='productAddToCartForm-80052967-50']//button"

    def get_selected_perfume_details(self):
        # Perfume name
        name = self.get_element_text(self._selected_parfum_name_xpath, "xpath")
        # Perfume Size.text
        size = self.get_element_text(self._selected_parfum_size_num_xpath, "xpath")
        unit = self.get_element_text(self._selected_parfum_size_unit_xpath, "xpath")
        # Perfume Price.text
        price = self.get_element_text(self._selected_parfum_price_xpath, "xpath")[:-1]

        details = [name, size, unit, price]
        print(f"Perfume Details :: {details}")
        self.log.info(f"Perfume Details :: {details}")
        return details

    def proceed_with_selection(self):
        self.element_click(self._perfume_select_button_xpath, "xpath")


