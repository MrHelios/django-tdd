from .base import FunctionalTest

from unittest import skip
from selenium.webdriver.common.keys import Keys

class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_text').send_keys(Keys.ENTER)

        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        self.browser.find_element_by_id('id_text').send_keys('Buy milk')
        self.browser.find_element_by_id('id_text').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        self.browser.find_element_by_id('id_text').send_keys(Keys.ENTER)
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))

        self.browser.find_element_by_id('id_text').send_keys('Make tea')
        self.browser.find_element_by_id('id_text').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_text').send_keys('Buy wellies')
        self.browser.find_element_by_id('id_text').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy wellies')

        self.browser.find_element_by_id('id_text').send_keys('Buy wellies')
        self.browser.find_element_by_id('id_text').send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            "You have already got this in your list"
        ))

    def test_error_messages_are_cleared_on_input(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_text').send_keys('Banter too thick')
        self.browser.find_element_by_id('id_text').send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Banter too thick')
        self.browser.find_element_by_id('id_text').send_keys('Banter too thick')
        self.browser.find_element_by_id('id_text').send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        self.browser.find_element_by_id('id_text').send_keys('a')

        # Cuando empezas a escribir nuevamente el mensaje se borra.
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))
