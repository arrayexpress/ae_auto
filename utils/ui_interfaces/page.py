import random
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import time
from os import environ
__author__ = 'Ahmed G. Ali'


class BasePage(object):
    """
    BasePage class extends object, it only initiates a new driver.
    """

    def __init__(self, url):
        environ['NO_PROXY'] = '127.0.0.1'
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
            "(KHTML, like Gecko) Chrome/15.0.87"
        )

        try:
            self.driver = webdriver.PhantomJS(desired_capabilities=dcap,
                                              service_log_path='/tmp/%s_ghostdriver.log' % random.randint(1111, 9999),
                                              service_args=['--ignore-ssl-errors=true', '--ssl-protocol=tlsv1'])
            # self.driver=webdriver.Chrome()
            self.driver.get(url)
        except Exception, e:
            print e
            print "Couldn't open: " +  url
            print 'sleeping 10 sec'
            print '=' * 30
            time.sleep(10)
            self.__init__(url)
