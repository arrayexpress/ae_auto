from selenium.webdriver.common.by import By

__author__ = 'Ahmed G. Ali'

class ConanLocators(object):
    """
    Selenium locators for the Home page.
    """

    TASKS_QUEUE_TABLE = (By.ID, 'conan-queue-table')
    EMAIL = (By.ID, 'conan-user-email-address')
    SIGN_IN_BTN = (By.ID, 'conan-log-in-button')
    GREETINGS = (By.ID, 'conan-user-greeting')
    PIPELINE_SELECT = (By.ID, 'conan-submissions-pipeline-select')
    PROCESS_SELECT = (By.ID, 'conan-submissions-process-select')
    ACCESSION_TEXT = (By.ID, 'conan-submissions-parameter-Accession Number-input')
    GO_BTN = (By.ID, 'conan-submissions-button')
    SUBMIT_BTN = (By.CSS_SELECTOR, 'body > '
                                   'div:nth-child(5) > '
                                   'div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > '
                                   'div > button:nth-child(1)')


