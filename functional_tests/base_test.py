import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from accounts.models import User


class BaseTest(StaticLiveServerTestCase):

    def setUp(self):
        self.webdriver = webdriver.Firefox()
        url_server = os.getenv('URL_SERVER', self.live_server_url)
        if url_server:
            self.live_server_url = url_server

    def tearDown(self):
        self.webdriver.quit()

    def login_as_superuser(self):
        email = 'admin@minhoteca.net'
        password = 'admin@123456'
        user = User.objects.create_superuser(email, password)
        user.full_clean()
        user.save()
        self.webdriver.get(self.live_server_url + '/admin')
        input_user = self.webdriver.find_element(By.ID, 'id_username')
        input_user.send_keys(email)
        input_password = self.webdriver.find_element(By.ID, 'id_password')
        input_password.send_keys(password)
        input_password.submit()
