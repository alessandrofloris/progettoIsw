import time

from selenium.webdriver.common.by import By


def create_activity(self, trip_id, activity):
    activity_name = activity["name"]
    activity_description = activity["description"]
    activity_start_date = activity["start_date"]
    activity_end_date = activity["end_date"]

    url = self.live_server_url + "/addactivity/" + str(trip_id)
    self.driver.get(url)

    name_field = self.driver.find_element(By.NAME, "name")
    name_field.send_keys(activity_name)

    description_field = self.driver.find_element(By.NAME, "description")
    description_field.send_keys(activity_description)

    start_date_field = self.driver.find_element(By.NAME, "start_date")
    self.driver.execute_script("arguments[0].value = arguments[1]", start_date_field, activity_start_date)

    end_date_field = self.driver.find_element(By.NAME, "end_date")
    self.driver.execute_script("arguments[0].value = arguments[1]", end_date_field, activity_end_date)

    add_activity_button = self.driver.find_element(By.NAME, "add_activity")
    time.sleep(2)
    add_activity_button.click()
    time.sleep(2)