from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
import time

from utils.ui_interfaces.conan.conan_locators import ConanLocators
from utils.ui_interfaces.page import BasePage

__author__ = 'Ahmed G. Ali'


class ConanPage(BasePage):
    """
    Extends BasePage class.
    It is a holder for all the functionality for the homepage http://visual.ly/
    """

    def login(self, login_email):
        self.driver.find_element(*ConanLocators.EMAIL).send_keys(login_email)
        btn = self.driver.find_element(*ConanLocators.SIGN_IN_BTN)
        while not btn.is_enabled():
            continue
        btn.click()

        try:
            WebDriverWait(self.driver, 120).until(
                expected_conditions.text_to_be_present_in_element(
                    locator=ConanLocators.GREETINGS, text_='Log out'
                )
            )
            WebDriverWait(self.driver, 360).until(
                expected_conditions.visibility_of_element_located(
                    ConanLocators.PIPELINE_SELECT
                )
            )
            return True
        except:
            return False

    def load_experiment(self, accession):
        select = Select(self.driver.find_element(*ConanLocators.PIPELINE_SELECT))
        select.select_by_visible_text('Experiment Loading (Combined AE2/Atlas)')
        self.driver.find_element(*ConanLocators.ACCESSION_TEXT).send_keys(accession)
        self.driver.find_element(*ConanLocators.GO_BTN).click()
        submit_btn = self.driver.find_element(*ConanLocators.SUBMIT_BTN)
        WebDriverWait(self.driver, 3).until(
            expected_conditions.visibility_of(submit_btn)
        )
        submit_btn.click()
        WebDriverWait(self.driver, 20).until(
            expected_conditions.text_to_be_present_in_element(
                ConanLocators.TASKS_QUEUE_TABLE,
                accession
            )
        )

    def unload_experiment(self, accession):
        select = Select(self.driver.find_element(*ConanLocators.PIPELINE_SELECT))
        select.select_by_visible_text('AE2 Experiment Unloading')
        self.driver.find_element(*ConanLocators.ACCESSION_TEXT).send_keys(accession)
        self.driver.find_element(*ConanLocators.GO_BTN).click()
        submit_btn = self.driver.find_element(*ConanLocators.SUBMIT_BTN)
        WebDriverWait(self.driver, 3).until(
            expected_conditions.visibility_of(submit_btn)
        )
        submit_btn.click()
        WebDriverWait(self.driver, 20).until(
            expected_conditions.text_to_be_present_in_element(
                ConanLocators.TASKS_QUEUE_TABLE,
                accession
            )
        )

    def clean_experiment(self, accession):
        select = Select(self.driver.find_element(*ConanLocators.PIPELINE_SELECT))
        select.select_by_visible_text('AE2 Experiment Unloading')
        process_select = Select(self.driver.find_element(*ConanLocators.PROCESS_SELECT))
        process_select.select_by_visible_text('unload cleanup')
        self.driver.find_element(*ConanLocators.ACCESSION_TEXT).send_keys(accession)
        self.driver.find_element(*ConanLocators.GO_BTN).click()
        submit_btn = self.driver.find_element(*ConanLocators.SUBMIT_BTN)
        WebDriverWait(self.driver, 3).until(
            expected_conditions.visibility_of(submit_btn)
        )
        submit_btn.click()


if __name__ == '__main__':
    conan = ConanPage(url='http://banana.ebi.ac.uk:14054/conan2/')
    # conan = ConanPage(url='http://banana.ebi.ac.uk:14052/conan2-curator/')
    print conan.login(login_email='ahmed@ebi.ac.uk')
    # conan.clean_experiment('E-GEOD-67793')
    # exit()
    # conan.load_experiment('E-MTAB-3647')
