from selenium.webdriver.common.by import By
from .base_test import BaseTest
from accounts.models import User
import time


class UserAdminTest(BaseTest):

    def create_superuser(self, username, password):
        user = User.objects.create(email=username)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.email_confirmed = True
        user.is_active = True
        user.save()

    def test_supervisor_can_access_admin_area(self):
        # O usuário admin acessa a área administrativa do minhoteca e encontra
        # um formulário para fazer login no sistema.
        # ##################
        # The admin user accesses the administrative area of ​​minhoteca and
        # finds a form to log in to the system.
        self.webdriver.get(self.live_server_url + '/admin')

        header_text = self.webdriver.find_element(By.TAG_NAME, 'h1').text
        self.assertIn(header_text, 'Django administration')

        # O usuário verifica que há um campo para que seja digitado o email...
        # ##################
        # The user verifies that there is a field for entering the email...
        input_user = self.webdriver.find_element(By.ID, 'id_username')
        self.assertTrue(input_user.is_displayed())

        # ... e um campo para que seja digitada a senha.
        # ##################
        # ... and a field for entering the password.
        time.sleep(5)
        input_password = self.webdriver.find_element(By.ID, 'id_password')
        self.assertTrue(input_password.is_displayed())

        # Também há um botão para confirmar o login.
        # ##################
        # There is also a button to confirm the login.
        button = self.webdriver.find_element(
            By.CSS_SELECTOR,
            'input[type=submit]')
        self.assertTrue(button.is_displayed())

    def test_can_login_with_valid_credentials(self):
        _username = 'minhoteca@test.net'
        _password = User.objects.make_random_password()
        self.create_superuser(_username, _password)

        # O usuário administrador preenche o formulário de login e clica no
        # botão de confirmação.
        # ##################
        # The admin user fills the login form and clicks the confirmation
        # button.
        self.webdriver.get(self.live_server_url + '/admin')
        input_user = self.webdriver.find_element(By.ID, 'id_username')
        input_user.send_keys(_username)
        input_password = self.webdriver.find_element(By.ID, 'id_password')
        input_password.send_keys(_password)
        button = self.webdriver.find_element(
            By.CSS_SELECTOR,
            'input[type=submit]')
        button.click()

        # Então é direcionado para a área administrativa do minhoteca.
        # ##################
        # Then it is directed to the administrative area of minhoteca.
        self.assertIn('admin', self.webdriver.title)
        self.assertIn('Django administration', self.webdriver.find_element(
            By.TAG_NAME, 'h1').text)

    def test_cant_login_with_INVALID_credentials(self):
        # O usuário administrador foi descuidado e um outro usuário, comum,
        # o viu fazendo login e pensa que também conseguirá acessar a área
        # administrativa do minhoteca.
        ##################
        # The admin user was careless and another common user saw him doing
        # login and thought that he could also access the administrative area
        # of minhoteca.
        _username = 'minhoteca@test.net'
        _password = User.objects.make_random_password()
        _invalid_username = 'minhoteca@test.com'
        _invalid_password = User.objects.make_random_password()
        self.create_superuser(_username, _password)

        # O usuário comum preenche o formulário de login e clica no botão.
        # ##################
        # The common user fills the login form and clicks the button.
        self.webdriver.get(self.live_server_url + '/admin')
        input_user = self.webdriver.find_element(By.ID, 'id_username')
        input_user.send_keys(_invalid_username)
        input_password = self.webdriver.find_element(By.ID, 'id_password')
        input_password.send_keys(_invalid_password)
        button = self.webdriver.find_element(
            By.CSS_SELECTOR,
            'input[type=submit]'
        )
        button.click()

        # Mas o sistema exibe uma mensagem de erro, informando que o login é
        # inválido.
        # ##################
        # But the system displays an error message, informing that the login is
        # invalid.
        errornote = self.webdriver.find_element(By.CLASS_NAME, 'errornote')
        self.assertIn(
            'Please enter the correct email and password for a staff account. '
            'Note that both fields may be case-sensitive.', errornote.text)

    def test_cant_login_with_VALID_user_but_wrong_password(self):
        _username = 'minhoteca@test.net'
        _password = User.objects.make_random_password()
        _invalid_password = User.objects.make_random_password()
        self.create_superuser(_username, _password)

        # O usuário comum é mal intencionado e tendo visto o email do usuário
        # administrador, faz uma nova tentativa de login com esse email e uma
        # senha que ela acha que é a correta.
        # ###################
        # The common user is malintentioned and saw the email of the admin
        # user, so he tries to login with that email and a password that she
        # thinks is correct.
        self.webdriver.get(self.live_server_url + '/admin')
        input_user = self.webdriver.find_element(By.ID, 'id_username')
        input_user.send_keys(_username)
        input_password = self.webdriver.find_element(By.ID, 'id_password')
        input_password.send_keys(_invalid_password)
        button = self.webdriver.find_element(
            By.CSS_SELECTOR,
            'input[type=submit]'
        )
        button.click()

        # Novamente o sistema exibe uma mensagem de erro.
        # ###################
        # Again the system displays an error message.
        errornote = self.webdriver.find_element(By.CLASS_NAME, 'errornote')
        self.assertIn(
            'Please enter the correct email and password for a staff account. '
            'Note that both fields may be case-sensitive.', errornote.text)

# from unittest.mock import Mock
