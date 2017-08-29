from selenium.webdriver.common.by import By

__author__ = 'Ahmed G. Ali'

class OtrsLocators(object):
    """
    Selenium locators for the Home page.
    """
    GREETINGS = (By.XPATH,'/html/body/table[1]/tbody/tr/td[2]')
    USER_NAME = (By.NAME, 'User')
    PASSWORD = (By.NAME, 'Password')
    SIGN_IN_BTN = (By.XPATH, '/html/body/center/form[1]/table/tbody/tr[2]/td/input')

    # TASKS_QUEUE_TABLE = (By.ID, 'conan-queue-table')
    # EMAIL = (By.ID, 'conan-user-email-address')
    # GREETINGS = (By.ID, 'conan-user-greeting')
    # PIPELINE_SELECT = (By.ID, 'conan-submissions-pipeline-select')
    # PROCESS_SELECT = (By.ID, 'conan-submissions-process-select')
    # ACCESSION_TEXT = (By.ID, 'conan-submissions-parameter-Accession Number-input')
    # GO_BTN = (By.ID, 'conan-submissions-button')
    # SUBMIT_BTN = (By.CSS_SELECTOR, 'body > '
    #                                'div:nth-child(5) > '
    #                                'div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > '
    #                                'div > button:nth-child(1)')


