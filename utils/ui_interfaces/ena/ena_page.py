
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

from utils.ui_interfaces.ena.ena_locators import ENALocators
from utils.ui_interfaces.page import BasePage

__author__ = 'Ahmed G. Ali'


class ENAPage(BasePage):
    """
    Extends BasePage class.
    It is a holder for all the functionality for the homepage http://visual.ly/
    """

    def login(self, user_name, password):
        self.driver.find_element(*ENALocators.USER_NAME).send_keys(user_name)
        self.driver.find_element(*ENALocators.PASSWORD).send_keys(password)
        btn = self.driver.find_element(*ENALocators.SIGN_IN_BTN)
        while not btn.is_enabled():
            continue
        btn.click()

        try:
            WebDriverWait(self.driver, 3).until(
                expected_conditions.text_to_be_present_in_element(
                    locator=ENALocators.LOGGED_IN, text_='Webin-24'
                )
            )
            return True
        except:
            return False


if __name__ == '__main__':
    ena = ENAPage(url='https://www.ebi.ac.uk/ena/submit/sra/#home')
    print ena.login(user_name='era-drop-24', password='lCV82ecg')
