from selenium.webdriver.common.by import By

__author__ = 'Ahmed G. Ali'

class ENALocators(object):
    """
    Selenium locators for the Home page.
    """

    USER_NAME = (By.CSS_SELECTOR, '#gwt-debug-usernameField > input')
    PASSWORD = (By.CSS_SELECTOR, '#gwt-debug-passwordField > input')
    SIGN_IN_BTN = (By.ID, 'gwt-debug-loginButton')
    LOGGED_IN = (By.CLASS_NAME, 'loggedNameLabel')

    SEARCH_BOX = (By.CSS_SELECTOR, '#sra-webin > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > div > div:nth-child(3) > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(1) > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr > td:nth-child(2) > input')
    SEARCH_BTN = (By.CSS_SELECTOR, '#sra-webin > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > div > div:nth-child(3) > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(1) > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr > td:nth-child(3) > img')

    EDIT_BTN = (By.CSS_SELECTOR, '#sra-webin > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > div > div:nth-child(3) > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(4) > td > table > tbody:nth-child(4) > tr > td:nth-child(8) > div > div > img')