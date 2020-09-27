from pages.PerfumeSelection import PerfumeSelection
from pages.PerfumeDetailBeforeFinalSelection import SelectPerfumeToAddToCart
from pages.GetDetailsBeforeAddingToCart import DetailBeforeAdditionToCart
from pages.PerfumeDetailFromCart import PerfumeDetailsFromCart
import unittest
import time
import pytest
global MainPageTitle


@pytest.mark.usefixtures("oneTimeSetUp")
class Test(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def classSetup(self):
        self.ps = PerfumeSelection(self.driver)
        self.bfs = SelectPerfumeToAddToCart(self.driver)
        self.batc = DetailBeforeAdditionToCart(self.driver)
        self.aatc = PerfumeDetailsFromCart(self.driver)

    @pytest.mark.run(order=1)
    def test_perfume_selection(self):
        global MainPageTitle
        self.ps.accept_cookies()
        time.sleep(2)
        MainPageTitle = self.ps.get_page_title()

        assert self.ps.navigate_to_product("perfume") is True
        assert self.ps.select_perfume("Tom Ford") is True

    @pytest.mark.run(order=2)
    def test_verify_name_and_cost_of_selected_perfume(self):
        selected_perfume_details = self.bfs.get_selected_perfume_details()
        self.bfs.proceed_with_selection()

        get_details_before_adding_to_cart = self.batc.get_detail_before_adding_cart()
        self.batc.proceed_with_selection()

        get_perfume_detail_from_cart = self.aatc.get_perfume_detail_from_cart()
        # get_perfume_detail_from_cart = ['Tom Ford', '50', 'ml', '70,95 €*']

        assert selected_perfume_details == get_details_before_adding_to_cart, f'Mismatch in Selected Perfume Details' \
                                                                              f' and Before adding to Cart page :: ' \
                                                                              f'{selected_perfume_details},' \
                                                                              f'{get_details_before_adding_to_cart}'
        assert get_details_before_adding_to_cart == get_perfume_detail_from_cart, f'Mismatch in Details Before and ' \
                                                                                  f'After adding to Cart :: ' \
                                                                                  f'{get_details_before_adding_to_cart}'\
                                                                                  f'{get_perfume_detail_from_cart}'
        assert selected_perfume_details == get_perfume_detail_from_cart, f'Mismatch in Selected Perfume Details and ' \
                                                                         f'After adding to Cart :: ' \
                                                                         f'{selected_perfume_details}'\
                                                                         f'{get_perfume_detail_from_cart}'

        print(selected_perfume_details)
        print(get_details_before_adding_to_cart)
        print(get_perfume_detail_from_cart)

    @pytest.mark.run(order=3)
    def test_mainmenu_navigation_link(self):
        global MainPageTitle
        self.aatc.navigate_to_main_page()
        main_pagetitle_after = self.aatc.get_page_title()
        print(MainPageTitle)
        print(main_pagetitle_after)
        assert MainPageTitle == main_pagetitle_after, f'Page title before is {MainPageTitle} and' \
                                                      f' page title after is {main_pagetitle_after}'



