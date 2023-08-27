import time

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


def new_invitation(self, invitation):
    invitation_recipient = invitation["recipient"]
    invitation_trip_name = invitation["trip"]

    self.driver.get(self.live_server_url + "/invite")

    email_field = self.driver.find_element(By.NAME, "recipient_email")
    email_field.send_keys(invitation_recipient)

    trip_name_field = self.driver.find_element(By.NAME, "trip")
    select = Select(trip_name_field)
    for option in select.options:
        if option.text == invitation_trip_name.name:
            option.click()
            break

    new_invite_button = self.driver.find_element(By.NAME, "new_invite")
    new_invite_button.click()


def process_invitation(self, accept):
    self.driver.get(self.live_server_url + "/invite")

    if accept:
        button = self.driver.find_element(By.NAME, "accept")
    else:
        button = self.driver.find_element(By.NAME, "decline")

    time.sleep(2)
    button.click()
    time.sleep(2)
