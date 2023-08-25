from django.test import LiveServerTestCase
from selenium import webdriver
from django.conf import settings
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

def test_new_trip_creation(self):
    # user navigates to the new trip creation page
    self.browser.get(self.live_server_url + '/newtrip')

    # user fills in the form fields
    name_input = self.browser.find_element_by_id('id_name')  # Replace with actual form field ID
    name_input.send_keys('My Trip')

    destination_input = self.browser.find_element_by_id('id_destination')
    destination_input.send_keys('My Destination')

    departure_date_input = self.browser.find_element_by_id('id_departure_date')
    departure_date_input.send_keys('2023-08-01')

    arrival_date_input = self.browser.find_element_by_id('id_arrival_date')
    arrival_date_input.send_keys('2023-08-10')

    # user submits the form
    create_button = self.browser.find_element_by_name('create_button')
    create_button.send_keys(Keys.RETURN)

    # user is redirected to the mytrips page (assert the redirect)
    self.assertIn('mytrips', self.browser.current_url)

    # Checking that the trip was created and displayed on the mytrips page
    self.assertIn('My Trip', self.browser.page_source)
    self.assertIn('My Destination', self.browser.page_source)
    self.assertIn('2023-08-01', self.browser.page_source)
    self.assertIn('2023-08-10', self.browser.page_source)

