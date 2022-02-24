import os
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class BaseTest(StaticLiveServerTestCase):

    def setUp(self):
        self.webdriver = webdriver.Firefox()
        url_server = os.getenv('URL_SERVER', self.live_server_url)
        if url_server:
            self.live_server_url = url_server

    def tearDown(self):
        self.webdriver.quit()
