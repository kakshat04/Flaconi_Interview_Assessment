from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyperclip
import json
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains
from Project.utility.read_from_json import ReadJson


baseURL = "https://demo-eu.leanix.net/akkDemo/"
driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(3)
driver.get(baseURL)

element = driver.find_element_by_name("j_username")
element.send_keys("kumar.akshat04@gmail.com")

sleep(1)

element = driver.find_element_by_name("j_password")
element.send_keys("Knight@riders1")

sleep(1)

driver.find_element_by_xpath("//button[contains(text(),'Login')]").click()
sleep(2)

# driver.find_element_by_id("menuLink").click()
# sleep(2)

driver.find_element(By.XPATH, "//span[contains(text(),'AWS IAM Users with Access Key Age')]").click()
sleep(5)

_age_limit_list = []
elements = driver.find_elements(By.XPATH, "//span[contains(@class,'viewLabel')]")
print(len(elements))
for element in elements:
    _age_limit_list.append(element.text)
print(_age_limit_list)

_verification_lst = []
for age in range(len(_age_limit_list)):
    if _age_limit_list[age] == 'n/a' or _age_limit_list[age] == '0':
        continue
    _verification_lst.append(int(_age_limit_list[age].split(" ")[1]) + 1)
print(_verification_lst)

_age_map = {}
# Now I have a make a dynamic Dict as per age range
for i in _age_limit_list:
    _age_color = "//span[contains(@class,'viewLabel') and text()='{0}']//preceding-sibling::span"
    _age_color_locator = _age_color.format(i)
    # print(_age_color_locator)
    # print(driver.find_element(By.XPATH, _age_color_locator).get_attribute("style"))
    _age_map[i] = _age_color_locator
print(_age_map)  # This is dynamic XPATH based on age range

attr_dict = {}

# Read user ages from json - list
json_read = ReadJson()
property_details_dict = json_read.get_user_property_details()

print("Dictionary of ADK_Name and AccessKeyAge received from JSON File..")
print(property_details_dict)

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
        age_index = _verification_lst.index(num) + 2

        # dictionary - age:xpath -- bg color
        xpath = _age_map[_age_limit_list[age_index]]

    # Find age bg color on report based on xpath
    element = driver.find_element(By.XPATH, xpath)
    attr_dict[adk] = element.get_attribute("style")  # {adk_name: style} from age range

print("Dictionary of ADK_Name(from json) and respective age limit Style value(in the report)..")
print(attr_dict)

# {'leanIXScanAgentUser': 'background-color: rgb(48, 105, 141);', 'LeanIXAccessLDIFBucket': 'background-color: rgb(191, 224, 245);'}