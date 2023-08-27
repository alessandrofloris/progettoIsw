
import time

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


def new_comment(self, comment):
    comment_content = comment["content"]
    comment_id_trip = comment["trip"].id

    url = self.live_server_url + "/viewtrip/" + str(comment_id_trip)
    self.driver.get(url)

    email_field = self.driver.find_element(By.NAME, "content")
    email_field.send_keys(comment_content)

    new_invite_button = self.driver.find_element(By.NAME, "add_comment")
    new_invite_button.click()


