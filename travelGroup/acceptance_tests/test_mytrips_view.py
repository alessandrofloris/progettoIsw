from . import utility_test
from selenium import webdriver
from travelGroup.models import CustomUser
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class MyTripsTest(StaticLiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.user = CustomUser.objects.create_superuser(username='testuser', first_name='test', last_name='user', email='testemail@email.com',
                               password='testpassword')
        self.user.save()

    def testLogin(self):
        utility_test.login(self.driver, self.live_server_url, "testuser", "testpassword")
        self.assertEqual(self.driver.current_url, self.live_server_url + "/mytrips")