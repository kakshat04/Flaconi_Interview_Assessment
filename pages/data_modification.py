from time import sleep
from Project.base.selenium_driver import SeleniumDriver as SD
from Project.utility.write_to_json import WriteJson
from Project.utility.custom_logging import custom_logger as cl
import os
import logging


class DataModification(SD):
    log = cl(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        # self.sd = SD(self.driver)

    # locators
    _user_image_id = "menuLink"
    _administration_drop_down_xpath = "//div[@id='appNavbarCollapse']//span[text()='Administration']"
    _integration_api_xpath = "//a[contains(@class,'integrationApiLink')]"
    _user_connector = "//a[contains(text(),'cloudockit')]"
    _inbound_text_area_xpath = "/html/body//div[2]/div[2]/div[1]//div[1]/textarea"
    _run_button_xpath = "//button[contains(text(),'Run')]"

    def navigate_integration_api(self):
        try:
            print("Now, after successful report validation, moving to data enhancement... :)")
            self.log.info("Now, after successful report validation, moving to data enhancement... :)")
            print("Navigating to Administration Page now..")
            self.log.info("Navigating to Administration Page now..")

            # Click on profile image
            self.element_click(self._user_image_id, "id")
            sleep(1)

            # Select Administration from drop down
            self.element_click(self._administration_drop_down_xpath, 'xpath')
            sleep(1)

            print("Click on integration api tab...")
            self.log.info("Click on integration api tab...")
            # click on integration api tab
            self.element_click(self._integration_api_xpath, 'xpath')
            sleep(1)

            print("Click on user connector..")
            self.log.info("Click on user connector..")
            # Click on user connector
            self.element_click(self._user_connector, 'xpath')
            sleep(5)  # This wait if for processor data to load

            print("Navigation Successful...Inside 'CDK-AWS-IAM-User' connector")
            self.log.info("Navigation Successful...Inside 'CDK-AWS-IAM-User' connector")
            return True
        except Exception as Error:
            print("Navigation Failed...", Error)
            self.log.error("Navigation Failed...", Error)
            return False

    def data_modify_security_warn_level(self):
        """
        This method will update json file with required Security Warn Level, based on Access Key age
        "" for 0 .. 30 days
        "low" for 31 .. 60 days
        "medium" for more than 60 days
        """

        msg = "Modifying json file as following - '' for 0-30 days, 'low' for 31-60 days, 'medium' for >60 days"
        print(msg)
        self.log.info(msg)

        # Modify data with required security warn levels
        modify_json = WriteJson()
        json_data, age_security_warn_dict = modify_json.write_security_warn_level()
        sleep(2)

        # This is done to load dict to os environment and used for verification in data_modification_check file
        os.environ['age_security_warn_dict'] = str(age_security_warn_dict)

        print("Json file modified with respective Security Warn Levels....")
        self.log.info("Json file modified with respective Security Warn Levels....")

        # update in inbound
        print("Copying Json to inbound...")
        self.log.info("Copying Json to inbound...")
        self.enter_text_in_textarea(self._inbound_text_area_xpath, 'xpath', json_data)

        sleep(2)
        print("Json Copying Successfully...")
        self.log.info("Json Copying Successfully...")

        # click on run -- RUN is enabled if proper json is loaded  ==> Code needs to be modified
        print("Verify if JSON file is loaded successfully..")
        self.log.info("Verify if JSON file is loaded successfully..")
        run_button_status = self.is_element_enabled(self._run_button_xpath, 'xpath')
        if run_button_status:
            print("Click on RUN..")
            self.log.info("Click on RUN..")
            self.element_click(self._run_button_xpath, 'xpath')

            print("Waiting for Run to complete")
            self.log.info("Waiting for Run to complete")
            sleep(12)

            # if run successful, return True else False
            print("Data Loaded Successfully...")
            self.log.info("Data Loaded Successfully...")
            return True
        else:
            self.log.error("JSON file is not loaded successfully..")
            return False








