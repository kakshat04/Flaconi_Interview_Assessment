from Project.pages.login_pages import LoginPage
from Project.pages.data_modification import DataModification
from Project.pages.data_modification_check import DataModificationCheck
from Project.pages.report_test import ReportTest
import unittest
import time
import pytest


@pytest.mark.usefixtures("oneTimeSetUp")
class LoginTest(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def classSetup(self):
        self.lp = LoginPage(self.driver)
        self.dm = DataModification(self.driver)
        self.dmc = DataModificationCheck(self.driver)
        self.rt = ReportTest(self.driver)

    # @pytest.mark.run(order=1)
    # def test_invalid_login(self):
    #     self.lp.login_page(email="invalidemail@gmail.com", password="invalid_password")
    #     time.sleep(2)
    #     assert self.lp.verify_login_failed() is True  # Verify login not successful

    @pytest.mark.run(order=2)
    def test_valid_login(self):
        self.lp.login_page(email="kumar.akshat04@gmail.com", password="Knight@riders1")
        time.sleep(1)
        assert self.lp.verify_login_successful() is True  # Verify login successful

    @pytest.mark.run(order=3)
    def test_check_report(self):
        self.rt.goto_iam_users()
        assert self.rt.verify_result_report() is True

    # @pytest.mark.run(order=4)
    # def test_data_modification(self):
    #     assert self.dm.navigate_integration_api() is True
    #     assert self.dm.data_modify_security_warn_level() is True
    #
    # @pytest.mark.run(order=5)
    # def test_modification_check(self):
    #     assert self.dmc.validate_leanix_scan_agent_user() is True
    #     assert self.dmc.validate_leanix_access_ldif_bucket() is True
