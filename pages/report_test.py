from time import sleep
from Project.base.selenium_driver import SeleniumDriver as SD
from Project.utility.read_from_json import ReadJson
from Project.utility.custom_logging import custom_logger as cl
import logging


class ReportTest(SD):
    log = cl(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        # self.sd = SD(self.driver)

    """
    ------------------------- OLD CODE -------------------------------------
    # age_mapping  --> {age range: xpath}
    _age_map = {
                   'n/a': "//span[contains(@class,'circle withBorder') and contains(@style,'rgb(255, 255, 255)')]",
                   '0': "//span[contains(@class,'circle') and contains(@style,'rgb(239, 239, 239)')]",
                   '> 0': "//span[contains(@class,'circle') and contains(@style,'rgb(191, 224, 245)')]",
                   '> 12': "//span[contains(@class,'circle') and contains(@style,'rgb(143, 184, 210)')]",
                   '> 24': "//span[contains(@class,'circle') and contains(@style,'rgb(96, 145, 176)')]",
                   '> 36': "//span[contains(@class,'circle') and contains(@style,'rgb(48, 105, 141)')]",
                   '> 48': "//span[contains(@class,'circle') and contains(@style,'rgb(0, 65, 106)')]",
                   '> 60': "//span[contains(@class,'circle') and contains(@style,'rgb(0, 65, 106)')]"
    }
    _age_limit_list = ['n/a', '0', '> 0', '> 12', '> 24', '> 36', '> 48', '> 60']
    _verification_lst = [1, 13, 25, 37, 49, 61]
        ------------------------- OLD CODE -------------------------------------
    """

    _iamuser_page_title = "AWS IAM Users with Access Key Age | LeanIX"

    # locators
    _iamusers_field_xpath = "//span[contains(text(),'AWS IAM Users with Access Key Age')]"
    _age_elements_xpath = "//span[contains(@class,'viewLabel')]"
    _leanix_ldif_bucket_xpath = "//div[contains(@class,'ClusterMap-contentItem') and " \
                                "contains(@title,'LeanIXAccessLDIFBucket')]"
    _leanix_scan_user_xpath = "//div[contains(@class,'ClusterMap-contentItem') and" \
                              " contains(@title,'leanIXScanAgentUser')]"

    def goto_iam_users(self):
        # scroll to
        self.scroll_to(self._iamusers_field_xpath, "xpath")
        sleep(1)
        self.execute_javascript("window.scrollBy(0,200)")
        sleep(3)

        # click
        self.element_click(self._iamusers_field_xpath, "xpath")
        sleep(5)

    def get_age_range_in_report(self):
        _age_limit_list = []
        elements = self.get_elements(self._age_elements_xpath, "xpath")
        print(len(elements))
        for element in elements:
            _age_limit_list.append(element.text)
        print(_age_limit_list)  # ['n/a', '0', '> 0', '> 18', '> 36', '> 54', '> 72', '> 90'] (as per current report)

        _verification_lst = []  # Creating list of age from age range
        for age in range(len(_age_limit_list)):
            if _age_limit_list[age] == 'n/a' or _age_limit_list[age] == '0':
                continue
            _verification_lst.append(int(_age_limit_list[age].split(" ")[1]) + 1)
        print(_verification_lst)  # [1, 19, 37, 55, 73, 91]

        return _age_limit_list, _verification_lst

    def create_xpath_for_age_range_color(self):
        _age_map = {}
        _age_limit_list, _verification_lst = self.get_age_range_in_report()

        # Now I have to make a dynamic Dict of age range and respective bg color
        for i in _age_limit_list:
            _age_color = "//span[contains(@class,'viewLabel') and text()='{0}']//preceding-sibling::span"
            _age_color_locator = _age_color.format(i)
            # print(_age_color_locator)
            # print(driver.find_element(By.XPATH, _age_color_locator).get_attribute("style"))
            _age_map[i] = _age_color_locator
        print(_age_map)  # This is dynamic XPATH based on age range
        # {'n/a': "//span[contains(@class,'viewLabel') and text()='n/a']//preceding-sibling::span",
        # '0': "//span[contains(@class,'viewLabel') and text()='0']//preceding-sibling::span",
        # '> 0': "//span[contains(@class,'viewLabel') and text()='> 0']//preceding-sibling::span",
        # '> 18': "//span[contains(@class,'viewLabel') and text()='> 18']//preceding-sibling::span" ....
        # ... '> 90': "//span[contains(@class,'viewLabel') and text()='> 90']//preceding-sibling::span"}

        return _age_map, _age_limit_list, _verification_lst

    def get_age_attribute_bg_clr(self):
        attr_dict = {}

        # Get dynamic xpath for each age range color code
        _age_map, _age_limit_list, _verification_lst = self.create_xpath_for_age_range_color()

        # Read user ages from json - list
        json_read = ReadJson()
        property_details_dict = json_read.get_user_property_details()

        print("Dictionary of ADK_Name and AccessKeyAge received from JSON File..")
        self.log.info("Dictionary of ADK_Name and AccessKeyAge received from JSON File..")
        print(property_details_dict)  # {'leanIXScanAgentUser': '74', 'LeanIXAccessLDIFBucket': '38'}
        self.log.info(property_details_dict)

        # Verify the age falls in which category of _age_limit_list
        # Verify range in report - index + 2
        for adk, age in property_details_dict.items():
            if age == 'n/a':
                xpath = _age_map['n/a']
            elif age == '0':
                # If age is n/a or 0
                xpath = _age_map['0']
            else:
                num = 0
                i = 0
                j = 0
                # print(age, num, i, j)
                while j < len(_verification_lst) - 1:
                    j += 1
                    if _verification_lst[i] <= int(age) < _verification_lst[j]:
                        num = _verification_lst[i]
                        break
                    i += 1
                if num == 0:
                    num = _verification_lst[-1]

                # +2, as _age_limit_list is 2 more than _verification_lst
                age_index = _verification_lst .index(num) + 2

                # dictionary - age:xpath -- bg color
                xpath = _age_map[_age_limit_list[age_index]]

            # Find age bg color on report based on xpath
            attr_dict[adk] = self.get_attribute(xpath, 'xpath', 'style')  # {adk_name: style} from age range

        print("Dictionary of ADK_Name(from json) and respective age limit Style value(in the report)..")
        self.log.info("Dictionary of ADK_Name(from json) and respective age limit Style value(in the report)..")
        print(attr_dict)
        self.log.info(attr_dict)
        # {'leanIXScanAgentUser': 'background-color: rgb(0, 65, 106);',
        # 'LeanIXAccessLDIFBucket': 'background-color: rgb(96, 145, 176);'}

        return attr_dict

    def get_aws_box_attribute_bg_clr(self):
        # AWS box bg color verify
        aws_box_user_lst = []
        user_age_color_dict = self.get_age_attribute_bg_clr()
        
        self.switch_to_frame(0)  # Switch Frame

        # Create Dynamic XPATH for users in AWS box
        for user, bg_clr in user_age_color_dict.items():
            aws_box_user_locator = "//div[contains(@title,'{0}') and contains(@style,'{1}')]"
            aws_box_user_lst.append(aws_box_user_locator.format(user, bg_clr))

        print(aws_box_user_lst)
        # ["//div[contains(@title,'leanIXScanAgentUser') and contains(@style,'background-color: rgb(0, 65, 106);')]",
        # "//div[contains(@title,'LeanIXAccessLDIFBucket') and contains(@style,'background-color: rgb(96, 145, 176);')]]

        return aws_box_user_lst, user_age_color_dict

    def verify_result_report(self):
        print("Make sure we navigated to the correct page, to avoid unnecessary executions")
        title = self.get_page_title()
        if self._iamuser_page_title in title:
            # age_attr_btn_dict = self.get_age_attribute_bg_clr()
            aws_box_user_lst, user_age_color_dict = self.get_aws_box_attribute_bg_clr()

            print("-----------------------")
            print(user_age_color_dict)
            # {'leanIXScanAgentUser': 'background-color: rgb(0, 65, 106);',
            # 'LeanIXAccessLDIFBucket': 'background-color: rgb(96, 145, 176);'}

            print(aws_box_user_lst)
            # ["//div[contains(@title,'leanIXScanAgentUser') and contains(@style,'background-color: rgb(0, 65, 106);')]",
            # "//div[contains(@title,'LeanIXAccessLDIFBucket') and contains(@style,'background-color: rgb(96, 145, 176);')]"]

            print("Verify if Dynamic Xpath created is present in DOM. If YES, bg color matched with age range and "
                  "user name matched ldif data..")
            for data in aws_box_user_lst:
                check_availability = self.is_element_present(data, "xpath")
                if not check_availability:
                    return False
            return True

