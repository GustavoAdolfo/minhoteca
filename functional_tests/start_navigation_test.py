from selenium.webdriver.common.by import By
from .base_test import BaseTest


class UserStartNavigationTest(BaseTest):

    # Usuário acessa o site e verifica que é exibida a página inicial da
    # Minhoteca.
    # ##################
    # The user accesses the site and verifies that is displayed the Minhoteca
    # home page.
    def test_user_can_access_home_page(self):
        self.webdriver.get(self.live_server_url)
        self.assertIn('Minhoteca', self.webdriver.title)
        title_minhoteca = self.webdriver.find_element(By.TAG_NAME, 'h1').text
        self.assertEqual(title_minhoteca, 'Minhoteca')

    # Usuário verifica que na página incial é exibida uma barra de navegação
    # com os seguintes itens: Livros, Autores, Entrar.
    # ##################
    # The user verifies that in the home page is displayed a navigation bar
    # with the following items: Livros, Autores, Entrar.
    def test_user_can_see_navigation_bar(self):
        self.webdriver.get(self.live_server_url)
        nav_bar = self.webdriver.find_element(By.CLASS_NAME, 'navbar')
        self.assertTrue(nav_bar)
        nav_links = nav_bar.find_elements(By.CLASS_NAME, 'nav-link')
        self.assertEqual(len(nav_links), 3)
        link_texts = [link.text for link in nav_links]
        self.assertTrue(all(link_text in link_texts for
                            link_text in ['Livros', 'Autores', 'Entrar']))
